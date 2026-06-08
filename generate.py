#!/usr/bin/env python3
"""
Generátor webu Dům Netušil — 14 bytů.

Spuštění:  python3 generate.py
Výstup:    index.html + byty/byt-XX.html (14×) + sitemap.xml
"""
from __future__ import annotations
import html
import json
import sys
from datetime import date
from pathlib import Path
from textwrap import dedent

SITE_URL = "https://dumnetusil.cz"  # mění se jen tady

# ---------------------------------------------------------------------------
# STATUS bytů — načítané ze status.json
# ---------------------------------------------------------------------------

ALLOWED_STATUSES = {"k dispozici", "rezervovano", "prodano"}

STATUS_META = {
    "k dispozici": {
        "label": "K dispozici",
        "color": "#3a7c4c",
        "bg": "#e6f0e9",
        "cta_text": "Sjednat prohlídku",
        "cta_disabled": False,
    },
    "rezervovano": {
        "label": "Rezervováno",
        "color": "#b8542b",
        "bg": "#fdeee5",
        "cta_text": "Rezervováno",
        "cta_disabled": True,
    },
    "prodano": {
        "label": "Prodáno",
        "color": "#6b2020",
        "bg": "#f1dada",
        "cta_text": "Prodáno",
        "cta_disabled": True,
    },
}


def load_statuses() -> dict:
    """Načti status.json, validuj hodnoty."""
    status_file = Path(__file__).parent / "status.json"
    if not status_file.exists():
        print(f"⚠ status.json nenalezen — všechny byty 'k dispozici'", file=sys.stderr)
        return {str(i).zfill(2): {"status": "k dispozici"} for i in range(1, 15)}

    data = json.loads(status_file.read_text())
    byty = data.get("byty", {})

    # Validace
    errors = []
    for aid, info in byty.items():
        s = info.get("status", "")
        if s not in ALLOWED_STATUSES:
            errors.append(f"  byt {aid}: neznámý status '{s}' (povoleno: {', '.join(ALLOWED_STATUSES)})")
    if errors:
        print("✗ Chyba ve status.json:", file=sys.stderr)
        print("\n".join(errors), file=sys.stderr)
        sys.exit(1)

    return byty


def load_ceny() -> dict:
    """Načti ceny.json, validuj že každý byt má cenu."""
    ceny_file = Path(__file__).parent / "ceny.json"
    if not ceny_file.exists():
        print(f"✗ ceny.json nenalezen — bez něj nelze web vygenerovat", file=sys.stderr)
        sys.exit(1)

    data = json.loads(ceny_file.read_text())
    byty = data.get("byty", {})

    # Validace
    errors = []
    for aid in [str(i).zfill(2) for i in range(1, 15)]:
        if aid not in byty:
            errors.append(f"  byt {aid}: chybí v ceny.json")
            continue
        info = byty[aid]
        if "cena_kc" not in info:
            errors.append(f"  byt {aid}: chybí pole 'cena_kc'")
        if "cena_kc_m2" not in info:
            errors.append(f"  byt {aid}: chybí pole 'cena_kc_m2'")
        # Validace, že cena_kc je číslo
        if "cena_kc" in info and not isinstance(info["cena_kc"], (int, float)):
            errors.append(f"  byt {aid}: cena_kc musí být číslo, je '{info['cena_kc']}'")
    if errors:
        print("✗ Chyba v ceny.json:", file=sys.stderr)
        print("\n".join(errors), file=sys.stderr)
        sys.exit(1)

    return byty

# ---------------------------------------------------------------------------
# DATA — 14 bytů
# ---------------------------------------------------------------------------

APARTMENTS = [
    {
        "id": "01", "patro": "1.NP", "patro_short": "1.NP",
        "dispozice": "2+kk", "plocha": 44.11,
        "extra": {"typ": "terasa", "plocha": 25.0, "popis": "Terasa 25 m²"},
        "tag": "S terasou",
        "headline": "2+kk se soukromou terasou",
        "headline_html": '2+kk <em>se soukromou</em><br>terasou do vnitrobloku',
        "lead": ("Největší byt v přízemí s privátní 25m² terasou orientovanou do klidného "
                 "vnitrobloku. Vlastní zelený prostor pro rána u kávy i letní večeře — "
                 "vzácnost v centru Brna."),
        "description": ("Byt 01 je nejlukrativnější jednotka v přízemí — kombinace 2+kk "
                        "s vlastní 25m² terasou, která se otevírá do tichého vnitrobloku. "
                        "Obývací pokoj s kuchyňským koutem (24,87 m²) je centrálním prostorem "
                        "bytu, ložnice nabízí klidné zázemí pro spánek.\n\n"
                        "Pro lidi, kteří chtějí v centru Brna vlastní outdoor prostor — "
                        "rodinu, pár se psem nebo investory cílící na prémiový nájem."),
        "rooms": [
            ("Obývací pokoj s kuchyňským koutem", "24,87 m²"),
            ("Ložnice", "10,20 m²"),
            ("Koupelna + WC", "~4 m²"),
            ("Předsíň", "~5 m²"),
            ("Terasa (privátní)", "25,00 m²"),
        ],
        "features": [
            "Privátní terasa 25 m² do vnitrobloku",
            "Otevřená dispozice obývák + KK",
            "Samostatná ložnice s oknem",
            "Koupelna s vanou a WC",
            "Tepelné čerpadlo",
        ],
        "images": ["1np-2kk.jpg", "1np-loznice-2kk.jpg", "ext-4.jpg"],
        "hero_img": "1np-2kk.jpg",
        "thumb_gradient": "linear-gradient(135deg,#a89b80,#7a6140)",
        "next_id": "02",
    },
    {
        "id": "02", "patro": "1.NP", "patro_short": "1.NP",
        "dispozice": "2+kk", "plocha": 36.45,
        "extra": None,
        "tag": "Přízemí",
        "headline": "2+kk s historickou fasádou",
        "headline_html": '2+kk <em>v přízemí</em><br>se zdobnou fasádou',
        "lead": ("Kompaktní dvoupokojový byt orientovaný do ulice. Okna se dotýkají "
                 "zachované zdobné fasády historického měšťanského domu. Vhodný pro dvojici "
                 "i jako investiční nemovitost s vyšším nájemným potenciálem."),
        "description": ("Byt 02 je kompaktní 2+kk v přízemí s okny do ulice — jen kousek od "
                        "zachované zdobné fasády. Otevřený obývací pokoj s kuchyňským koutem "
                        "(17,58 m²) propojuje denní život, samostatná ložnice nabízí klidné "
                        "zázemí.\n\n"
                        "Vhodný pro pár, jednotlivce nebo jako investiční byt s potenciálem "
                        "vyššího nájemného — přízemí v Husovicích je vyhledávané studenty MU "
                        "i mladými profesionály."),
        "rooms": [
            ("Obývací pokoj s kuchyňským koutem", "17,58 m²"),
            ("Ložnice", "9,81 m²"),
            ("Koupelna + WC", "~4 m²"),
            ("Předsíň", "~5 m²"),
        ],
        "features": [
            "Orientace do ulice s historickou fasádou",
            "Otevřená dispozice obývák + KK",
            "Samostatná ložnice s oknem",
            "Koupelna s vanou a WC",
            "Tepelné čerpadlo",
        ],
        "images": ["1np-2kk.jpg", "1np-loznice-2kk.jpg", "ext-1.jpg"],
        "hero_img": "1np-2kk.jpg",
        "thumb_gradient": "linear-gradient(135deg,#c8b89e,#9a8265)",
        "next_id": "03",
    },
    {
        "id": "03", "patro": "2.NP", "patro_short": "2.NP",
        "dispozice": "1+kk", "plocha": 25.64,
        "extra": {"typ": "balkón", "plocha": 4.45, "popis": "Balkón 4,45 m²"},
        "tag": "S balkonem",
        "headline": "1+kk s balkonem ve 2.NP",
        "headline_html": '1+kk <em>s balkonem</em><br>do vnitrobloku',
        "lead": ("Kompaktní 1+kk s balkonem do tichého vnitrobloku ve druhém patře. "
                 "Pro pár nebo individualistu, který hledá vlastní bydlení v centru Brna."),
        "description": ("Byt 03 je 1+kk s vlastním balkonem orientovaným do klidného "
                        "vnitrobloku. Otevřený obývák s kuchyňským koutem (16,20 m²) je "
                        "centrálním prostorem, balkon přidává outdoor.\n\n"
                        "Nejlikvidnější velikost pro pronájem v Husovicích — startovní bydlení, "
                        "menší investiční jednotka pro dlouhodobý pronájem."),
        "rooms": [
            ("Obývací pokoj s kuchyňským koutem", "16,20 m²"),
            ("Koupelna + WC", "~4 m²"),
            ("Předsíň", "~5 m²"),
            ("Balkón", "4,45 m²"),
        ],
        "features": [
            "Vlastní balkon 4,45 m² do vnitrobloku",
            "Otevřená dispozice obývák + KK",
            "Koupelna s vanou a WC",
            "Tepelné čerpadlo",
            "2. nadzemní patro — světlo a klid",
        ],
        "images": ["3np-1kk.jpg", "3np-1kk-2.jpg", "ext-4.jpg"],
        "hero_img": "3np-1kk.jpg",
        "thumb_gradient": "linear-gradient(135deg,#b5a487,#857258)",
        "next_id": "04",
    },
    {
        "id": "04", "patro": "2.NP", "patro_short": "2.NP",
        "dispozice": "2+kk", "plocha": 43.27,
        "extra": {"typ": "balkón", "plocha": 5.71, "popis": "Balkón 5,71 m²"},
        "tag": "S balkonem",
        "headline": "2+kk s balkonem",
        "headline_html": '2+kk <em>s balkonem</em><br>do klidného vnitrobloku',
        "lead": ("Dvoupokojový byt s balkonem do klidného vnitrobloku ve druhém patře. "
                 "Nejvyhledávanější dispozice v domě — pro startovní bydlení i malou rodinu."),
        "description": ("Byt 04 je klasický 2+kk s vlastním balkonem — dispozice, kterou hledá "
                        "většina kupujících. Velký obývák s kuchyňským koutem (20,59 m²), "
                        "samostatná ložnice (11,83 m²), prostorná koupelna a balkon do "
                        "tichého vnitrobloku.\n\n"
                        "Ideální startovní byt pro pár nebo malou rodinu. Nejnižší cena za m² "
                        "v domě v této dispozici."),
        "rooms": [
            ("Obývací pokoj s kuchyňským koutem", "20,59 m²"),
            ("Ložnice", "11,83 m²"),
            ("Koupelna + WC", "~4 m²"),
            ("Předsíň", "~5 m²"),
            ("Balkón", "5,71 m²"),
        ],
        "features": [
            "Vlastní balkon 5,71 m² do vnitrobloku",
            "Velký obývák s KK (20,59 m²)",
            "Samostatná ložnice",
            "Koupelna s vanou a WC",
            "Tepelné čerpadlo",
        ],
        "images": ["2np-2kk.jpg", "2np-loznice-2kk.jpg", "ext-4.jpg"],
        "hero_img": "2np-2kk.jpg",
        "thumb_gradient": "linear-gradient(135deg,#b8a384,#8a724f)",
        "next_id": "05",
    },
    {
        "id": "05", "patro": "2.NP", "patro_short": "2.NP",
        "dispozice": "1+kk", "plocha": 24.22,
        "extra": None,
        "tag": "Do ulice",
        "headline": "1+kk s pohledem do ulice",
        "headline_html": '1+kk <em>kompaktní</em><br>orientovaný do ulice',
        "lead": ("Kompaktní 1+kk orientovaný do ulice ve druhém patře. Nejmenší a nejdostupnější "
                 "byt v domě — ideální pro studenta nebo investora."),
        "description": ("Byt 05 je nejkompaktnější 1+kk v domě s okny do ulice. Otevřený "
                        "obývák s kuchyňským koutem (16,09 m²), samostatná koupelna a předsíň.\n\n"
                        "Nejnižší absolutní cena v domě — vstupní jednotka pro investora cílícího "
                        "na pronájem studentům nebo mladým profesionálům v Husovicích."),
        "rooms": [
            ("Obývací pokoj s kuchyňským koutem", "16,09 m²"),
            ("Koupelna + WC", "~4 m²"),
            ("Předsíň", "~5 m²"),
        ],
        "features": [
            "Orientace do ulice s historickou fasádou",
            "Otevřená dispozice obývák + KK",
            "Koupelna s vanou a WC",
            "Tepelné čerpadlo",
            "Nejdostupnější byt v domě",
        ],
        "images": ["3np-1kk-2.jpg", "3np-1kk-ii.jpg", "ext-1.jpg"],
        "hero_img": "3np-1kk-2.jpg",
        "thumb_gradient": "linear-gradient(135deg,#c2b394,#947d5d)",
        "next_id": "06",
    },
    {
        "id": "06", "patro": "2.NP", "patro_short": "2.NP",
        "dispozice": "1+kk", "plocha": 25.11,
        "extra": None,
        "tag": "Do vnitrobloku",
        "headline": "1+kk do tichého vnitrobloku",
        "headline_html": '1+kk <em>s tichým výhledem</em><br>do vnitrobloku',
        "lead": ("Kompaktní 1+kk s výhledem do klidného vnitrobloku ve druhém patře. "
                 "Optimální poměr velikosti, klidu a ceny."),
        "description": ("Byt 06 je 1+kk orientovaný do vnitrobloku — klid, který v centru "
                        "Brna nenajdete často. Otevřený obývák s kuchyňským koutem (16,11 m²), "
                        "samostatná koupelna a předsíň.\n\n"
                        "Vhodný pro člověka, který chce klid v centru — workout brain, "
                        "telework nebo prostě klidné bydlení."),
        "rooms": [
            ("Obývací pokoj s kuchyňským koutem", "16,11 m²"),
            ("Koupelna + WC", "~4 m²"),
            ("Předsíň", "~5 m²"),
        ],
        "features": [
            "Orientace do tichého vnitrobloku",
            "Otevřená dispozice obývák + KK",
            "Koupelna s vanou a WC",
            "Tepelné čerpadlo",
        ],
        "images": ["3np-1kk.jpg", "3np-1kk-ii.jpg", "ext-4.jpg"],
        "hero_img": "3np-1kk.jpg",
        "thumb_gradient": "linear-gradient(135deg,#aa9474,#7a6240)",
        "next_id": "07",
    },
    {
        "id": "07", "patro": "3.NP", "patro_short": "3.NP",
        "dispozice": "1+kk", "plocha": 25.64,
        "extra": {"typ": "balkón", "plocha": 4.45, "popis": "Balkón 4,45 m²"},
        "tag": "Investorský favorit",
        "headline": "1+kk s balkonem ve 3.NP",
        "headline_html": '1+kk <em>s balkonem</em><br>investorský favorit',
        "lead": ("Kompaktní 1+kk s balkonem do vnitrobloku. Nejlikvidnější velikost "
                 "pro pronájem v Brně — studenti MU i mladí profesionálové."),
        "description": ("Byt 07 je 1+kk se balkonem ve třetím patře — vyšší patro = více "
                        "světla a klidu od ulice. Otevřený obývák s kuchyňským koutem "
                        "(16,20 m²), balkon 4,45 m² do vnitrobloku.\n\n"
                        "Nejlepší investiční byt v domě podle analýzy nájemného trhu — "
                        "kombinace velikosti, vyššího patra a balkonu maximalizuje cenu "
                        "za nájem."),
        "rooms": [
            ("Obývací pokoj s kuchyňským koutem", "16,20 m²"),
            ("Koupelna + WC", "~4 m²"),
            ("Předsíň", "~5 m²"),
            ("Balkón", "4,45 m²"),
        ],
        "features": [
            "Vlastní balkon 4,45 m² do vnitrobloku",
            "3. nadzemní patro — světlo a klid",
            "Otevřená dispozice obývák + KK",
            "Koupelna s vanou a WC",
            "Tepelné čerpadlo",
        ],
        "images": ["3np-1kk.jpg", "3np-1kk-2.jpg", "ext-4.jpg"],
        "hero_img": "3np-1kk.jpg",
        "thumb_gradient": "linear-gradient(135deg,#9c8866,#6d5a40)",
        "next_id": "08",
    },
    {
        "id": "08", "patro": "3.NP", "patro_short": "3.NP",
        "dispozice": "2+kk", "plocha": 43.27,
        "extra": {"typ": "balkón", "plocha": 5.71, "popis": "Balkón 5,71 m²"},
        "tag": "S balkonem",
        "headline": "2+kk s balkonem ve 3.NP",
        "headline_html": '2+kk <em>s balkonem</em><br>ve vyšším patře',
        "lead": ("Dvoupokojový byt v třetím patře s balkonem do klidného vnitrobloku. "
                 "Klid s výškou — světlo a ticho jdou ruku v ruce."),
        "description": ("Byt 08 je 2+kk se vším co od bytu očekáváte — velký obývák s KK "
                        "(18,22 m²), samostatná ložnice (10,54 m²), balkon a vyšší patro.\n\n"
                        "Pro pár nebo malou rodinu, která chce klidnější bydlení s lepším "
                        "světlem než v nižších patrech."),
        "rooms": [
            ("Obývací pokoj s kuchyňským koutem", "18,22 m²"),
            ("Ložnice", "10,54 m²"),
            ("Koupelna + WC", "~4 m²"),
            ("Předsíň", "~5 m²"),
            ("Balkón", "5,71 m²"),
        ],
        "features": [
            "Vlastní balkon 5,71 m² do vnitrobloku",
            "Samostatná ložnice",
            "3. nadzemní patro — světlo a klid",
            "Koupelna s vanou a WC",
            "Tepelné čerpadlo",
        ],
        "images": ["2np-2kk.jpg", "2np-loznice-2kk.jpg", "ext-4.jpg"],
        "hero_img": "2np-2kk.jpg",
        "thumb_gradient": "linear-gradient(135deg,#a89473,#7a6442)",
        "next_id": "09",
    },
    {
        "id": "09", "patro": "3.NP", "patro_short": "3.NP",
        "dispozice": "1+kk", "plocha": 24.22,
        "extra": None,
        "tag": "Do ulice",
        "headline": "1+kk s historickou fasádou",
        "headline_html": '1+kk <em>v 3. patře</em><br>s pohledem do ulice',
        "lead": ("Kompaktní 1+kk ve třetím patře s okny do ulice. Vyšší patro — "
                 "lepší světlo a klid od pouličního ruchu."),
        "description": ("Byt 09 je 1+kk s okny do ulice ve třetím patře — výška mu dává klid "
                        "a více světla. Otevřený obývák s kuchyňským koutem (16,09 m²), "
                        "samostatná koupelna a předsíň.\n\n"
                        "Pro toho, kdo chce malý byt s charakterem — pohled do zdobné "
                        "historické fasády vlastního domu je vzácnost."),
        "rooms": [
            ("Obývací pokoj s kuchyňským koutem", "16,09 m²"),
            ("Koupelna + WC", "~4 m²"),
            ("Předsíň", "~5 m²"),
        ],
        "features": [
            "Orientace do ulice — pohled na historickou fasádu",
            "3. nadzemní patro — lepší světlo",
            "Otevřená dispozice obývák + KK",
            "Koupelna s vanou a WC",
            "Tepelné čerpadlo",
        ],
        "images": ["3np-1kk-ii.jpg", "3np-1kk.jpg", "ext-1.jpg"],
        "hero_img": "3np-1kk-ii.jpg",
        "thumb_gradient": "linear-gradient(135deg,#b59c75,#876d4a)",
        "next_id": "10",
    },
    {
        "id": "10", "patro": "3.NP", "patro_short": "3.NP",
        "dispozice": "1+kk", "plocha": 25.11,
        "extra": None,
        "tag": "Do vnitrobloku",
        "headline": "1+kk do tichého vnitrobloku",
        "headline_html": '1+kk <em>v 3. patře</em><br>s klidem vnitrobloku',
        "lead": ("Kompaktní 1+kk s výhledem do klidného vnitrobloku ve třetím patře. "
                 "Tichá lokalita s lepším světlem a klidem."),
        "description": ("Byt 10 je 1+kk orientovaný do vnitrobloku ve třetím patře. "
                        "Maximální ticho, lepší světlo než v nižších patrech, otevřený "
                        "obývák s KK (16,11 m²).\n\n"
                        "Pro toho, kdo prioritizuje klid — workfromhome, klidný spánek, "
                        "tichá lokalita uprostřed města."),
        "rooms": [
            ("Obývací pokoj s kuchyňským koutem", "16,11 m²"),
            ("Koupelna + WC", "~4 m²"),
            ("Předsíň", "~5 m²"),
        ],
        "features": [
            "Orientace do tichého vnitrobloku",
            "3. nadzemní patro — lepší světlo a klid",
            "Otevřená dispozice obývák + KK",
            "Koupelna s vanou a WC",
            "Tepelné čerpadlo",
        ],
        "images": ["3np-1kk-2.jpg", "3np-1kk-ii.jpg", "ext-4.jpg"],
        "hero_img": "3np-1kk-2.jpg",
        "thumb_gradient": "linear-gradient(135deg,#b09474,#806242)",
        "next_id": "11",
    },
    {
        "id": "11", "patro": "4.NP", "patro_short": "4.NP",
        "dispozice": "2+kk mezonet", "plocha": 43.57,
        "extra": {"typ": "balkón", "plocha": 7.26, "popis": "Balkón 7,26 m²"},
        "tag": "Podkroví · Top byt",
        "headline": "2+kk mezonet s největším balkonem",
        "headline_html": 'Podkrovní 2+kk <em>s největším</em><br>balkonem v domě',
        "lead": ("Mezonet 2+kk s největším balkonem v domě (7,26 m²) a charakteristickou "
                 "atmosférou zkosených stropů. Nejvyšší kvalita světla."),
        "description": ("Byt 11 je nejvyšší 2+kk v domě — mezonet ve čtvrtém patře pod "
                        "podkrovím s velkým balkonem (7,26 m²) a atmosférou zkosených stropů. "
                        "Obývák s KK (19,73 m²), ložnice (13,23 m²) — nejvyšší úroveň světla "
                        "v celém domě.\n\n"
                        "Pro toho, kdo chce v centru Brna výjimečný byt s podkrovní atmosférou — "
                        "rodina, designově vnímavý kupující, sběratel autentických prostor."),
        "rooms": [
            ("Obývací pokoj s kuchyňským koutem", "19,73 m²"),
            ("Ložnice", "13,23 m²"),
            ("Koupelna + WC", "~4 m²"),
            ("Předsíň", "~5 m²"),
            ("Balkón", "7,26 m²"),
        ],
        "features": [
            "Největší balkon v domě — 7,26 m²",
            "Mezonet — zkosené stropy",
            "Maximum světla v domě",
            "Samostatná ložnice",
            "Koupelna s vanou a WC",
            "Tepelné čerpadlo",
        ],
        "images": ["4np-2kk.jpg", "4np-loznice-2kk.jpg", "ext-4.jpg"],
        "hero_img": "4np-2kk.jpg",
        "thumb_gradient": "linear-gradient(135deg,#aa9472,#7d6a4f)",
        "next_id": "12",
    },
    {
        "id": "12", "patro": "4.NP", "patro_short": "4.NP",
        "dispozice": "1+kk", "plocha": 24.22,
        "extra": None,
        "tag": "Nejvyšší patro",
        "headline": "1+kk ve 4. patře",
        "headline_html": '1+kk <em>v nejvyšším</em><br>bytovém patře',
        "lead": ("1+kk v nejvyšším bytovém patře. Nejvyšší světelná kvalita a klid v domě."),
        "description": ("Byt 12 je 1+kk ve čtvrtém patře — vyšší patro znamená lepší světlo, "
                        "klid od ulice a oddálení od bezprostředního ruchu města. Otevřený "
                        "obývák s KK (16,09 m²), samostatná koupelna a předsíň.\n\n"
                        "Vyhledávaná velikost ve vyšším patře — investiční jednotka "
                        "s prémiovým nájemným potenciálem."),
        "rooms": [
            ("Obývací pokoj s kuchyňským koutem", "16,09 m²"),
            ("Koupelna + WC", "~4 m²"),
            ("Předsíň", "~5 m²"),
        ],
        "features": [
            "Nejvyšší bytové patro — maximum světla",
            "Orientace do ulice — pohled na fasádu",
            "Otevřená dispozice obývák + KK",
            "Koupelna s vanou a WC",
            "Tepelné čerpadlo",
        ],
        "images": ["4np-1kk.jpg", "3np-1kk-ii.jpg", "ext-1.jpg"],
        "hero_img": "4np-1kk.jpg",
        "thumb_gradient": "linear-gradient(135deg,#a08664,#6e5638)",
        "next_id": "13",
    },
    {
        "id": "13", "patro": "4.NP", "patro_short": "4.NP",
        "dispozice": "1+kk", "plocha": 25.11,
        "extra": None,
        "tag": "Nejvyšší patro",
        "headline": "1+kk do vnitrobloku ve 4.NP",
        "headline_html": '1+kk <em>v nejvyšším patře</em><br>s klidem vnitrobloku',
        "lead": ("1+kk ve čtvrtém patře s výhledem do vnitrobloku. Maximum klidu a světla."),
        "description": ("Byt 13 je 1+kk ve čtvrtém patře orientovaný do tichého vnitrobloku — "
                        "kombinace, kterou v centru města jen málokdo nabídne. Otevřený obývák "
                        "s KK (16,11 m²), samostatná koupelna a předsíň.\n\n"
                        "Pro toho, kdo prioritizuje klid v centru — workfromhome, "
                        "tichý spánek, oddálení od ruchu."),
        "rooms": [
            ("Obývací pokoj s kuchyňským koutem", "16,11 m²"),
            ("Koupelna + WC", "~4 m²"),
            ("Předsíň", "~5 m²"),
        ],
        "features": [
            "Nejvyšší bytové patro",
            "Orientace do tichého vnitrobloku",
            "Otevřená dispozice obývák + KK",
            "Koupelna s vanou a WC",
            "Tepelné čerpadlo",
        ],
        "images": ["4np-1kk.jpg", "3np-1kk-2.jpg", "ext-4.jpg"],
        "hero_img": "4np-1kk.jpg",
        "thumb_gradient": "linear-gradient(135deg,#ab8e6c,#735944)",
        "next_id": "14",
    },
    {
        "id": "14", "patro": "Podkroví", "patro_short": "5.NP",
        "dispozice": "3+kk", "plocha": 60.21,
        "extra": None,
        "tag": "Top patro",
        "headline": "3+kk v nejvyšším patře",
        "headline_html": 'Podkrovní 3+kk <em>největší</em><br>byt v domě',
        "lead": ("Největší jednotka v domě. Tři místnosti s kuchyňským koutem, světlem shora "
                 "a výhledem do okolí. Plnohodnotný byt v nejvyšším patře."),
        "description": ("Byt 14 je vlajková loď celého projektu — největší 3+kk v podkroví "
                        "s OBÝVACÍ POKOJEM (27,39 m²), šatnou, dvěma koupelnami a galerií. "
                        "Atmosféra zkosených stropů, světlo přicházející shora, "
                        "vyhlídka do okolí.\n\n"
                        "Pro rodinu, pár se zázemím pro hosta, nebo prémiového kupujícího, "
                        "který si v centru Brna chce dopřát výjimečný byt."),
        "rooms": [
            ("Obývací pokoj s kuchyňským koutem", "27,39 m²"),
            ("Hala", "~6 m²"),
            ("Galerie", "~10 m²"),
            ("Šatna", "3,61 m²"),
            ("Koupelna + WC", "~4 m²"),
            ("Sociální zázemí", "~5 m²"),
            ("Schodiště interní", "~5 m²"),
        ],
        "features": [
            "Největší byt v domě (60,21 m²)",
            "Podkrovní atmosféra — zkosené stropy",
            "Vlastní galerie",
            "Šatna",
            "Dva sociální celky",
            "Maximální množství světla",
        ],
        "images": ["4np-2kk.jpg", "4np-loznice-2kk.jpg", "ext-4.jpg"],
        "hero_img": "4np-2kk.jpg",
        "thumb_gradient": "linear-gradient(135deg,#b89c75,#8c7250)",
        "next_id": "01",
    },
]

# ---------------------------------------------------------------------------
# Pomocné funkce
# ---------------------------------------------------------------------------

def _fmt_kc(amount: int | float) -> str:
    """Format jako '5 066 550' (nezlomitelné mezery)."""
    return f"{amount:,.0f}".replace(",", " ")

def _fmt_m2(plocha: float) -> str:
    """Format jako '36,45'."""
    return f"{plocha:.2f}".replace(".", ",")

def _calc_total_price(a: dict) -> int:
    """Vrátí cenu bytu z konfigurace (ceny.json)."""
    return int(a["cena_kc"])

def _escape(s: str) -> str:
    """HTML-escape pro bezpečnost."""
    return html.escape(s, quote=True)

def _description_html(text: str) -> str:
    """Převede plain-text popis na HTML <p> bloky."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    return "\n        ".join(f"<p>{_escape(p)}</p>" for p in paragraphs)

# ---------------------------------------------------------------------------
# CSS — sdílený mezi všemi stránkami
# ---------------------------------------------------------------------------

SHARED_CSS = dedent("""
:root{
  --bg:#f7f5f1;
  --paper:#ffffff;
  --ink:#1b1b1b;
  --ink-soft:#4a4a4a;
  --ink-mute:#8a8478;
  --line:#e7e1d5;
  --accent:#7a6140;
  --accent-dark:#4d3f29;
  --brick:#b8542b;
  --serif:'Cormorant Garamond','Playfair Display',Georgia,'Times New Roman',serif;
  --sans:system-ui,-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
html,body{margin:0;padding:0;background:var(--bg);color:var(--ink);font-family:var(--sans);-webkit-font-smoothing:antialiased;line-height:1.6}
img{max-width:100%;display:block}
h1,h2,h3,h4{font-family:var(--serif);font-weight:500;letter-spacing:-.01em;line-height:1.1;margin:0 0 .4em}
h1{font-size:clamp(2.4rem,5vw,4.6rem);font-weight:400}
h2{font-size:clamp(1.8rem,3vw,2.6rem);font-weight:400}
h3{font-size:1.4rem}
p{margin:0 0 1em;color:var(--ink-soft)}
a{color:var(--accent-dark);text-decoration:none;border-bottom:1px solid transparent;transition:border-color .25s}
a:hover{border-color:var(--accent-dark)}
.wrap{max-width:1280px;margin:0 auto;padding:0 32px}
.wrap-wide{max-width:1440px;margin:0 auto;padding:0 32px}
.eyebrow{font-family:var(--sans);font-size:.78rem;text-transform:uppercase;letter-spacing:.22em;color:var(--accent);font-weight:700;margin-bottom:18px;display:inline-block}
.btn{display:inline-flex;align-items:center;gap:12px;padding:16px 30px;font-weight:600;font-size:.92rem;letter-spacing:.04em;text-transform:uppercase;border:1px solid transparent;cursor:pointer;font-family:var(--sans);text-decoration:none}
.btn-primary{background:var(--ink);color:#fff;border-color:var(--ink)}
.btn-primary:hover{background:var(--accent-dark);border-color:var(--accent-dark);color:#fff}
.btn-ghost{background:transparent;color:#fff;border:1px solid rgba(255,255,255,.75)}
.btn-ghost:hover{background:#fff;color:var(--ink);border-color:#fff}
.btn-outline{background:transparent;color:var(--ink);border:1px solid var(--ink)}
.btn-outline:hover{background:var(--ink);color:#fff}

nav.top{position:fixed;top:0;left:0;right:0;z-index:50;background:rgba(247,245,241,.96);backdrop-filter:blur(14px);border-bottom:1px solid var(--line);padding:18px 0}
nav.top .wrap{display:flex;align-items:center;justify-content:space-between}
nav.top .logo{font-family:var(--serif);font-size:1.5rem;font-weight:500;color:var(--ink);line-height:1;border:0}
nav.top .logo small{display:block;font-family:var(--sans);font-size:.62rem;letter-spacing:.28em;text-transform:uppercase;color:var(--ink-mute);font-weight:500;margin-top:4px}
nav.top ul{display:flex;gap:38px;list-style:none;margin:0;padding:0}
nav.top ul a{font-size:.84rem;color:var(--ink);font-weight:500;border:0;text-transform:uppercase;letter-spacing:.1em}
nav.top ul a:hover{color:var(--accent-dark)}
nav.top .back{font-size:.84rem;color:var(--ink);font-weight:500;text-transform:uppercase;letter-spacing:.1em;border:0}
nav.top .back:hover{color:var(--accent-dark)}
@media(max-width:900px){nav.top ul{display:none}}

footer{background:var(--ink);color:rgba(255,255,255,.6);padding:60px 0 40px;font-size:.86rem}
footer .wrap{display:grid;grid-template-columns:1.5fr 1fr 1fr;gap:48px}
@media(max-width:760px){footer .wrap{grid-template-columns:1fr;gap:30px}}
footer h4{font-family:var(--serif);color:#fff;font-size:1.2rem;margin-bottom:14px;font-weight:500}
footer p{color:rgba(255,255,255,.55);font-size:.86rem;margin-bottom:8px}
footer ul{list-style:none;padding:0;margin:0}
footer ul li{margin-bottom:8px}
footer ul a{color:rgba(255,255,255,.6);font-size:.86rem;border:0}
footer ul a:hover{color:#fff}
footer .legal{grid-column:1/-1;border-top:1px solid rgba(255,255,255,.1);padding-top:24px;margin-top:30px;font-size:.78rem;color:rgba(255,255,255,.4)}

.lightbox{position:fixed;inset:0;background:rgba(0,0,0,.95);display:none;align-items:center;justify-content:center;z-index:200;padding:40px;cursor:zoom-out}
.lightbox.open{display:flex}
.lightbox img{max-width:100%;max-height:100%;cursor:default}
.lightbox .close{position:absolute;top:24px;right:32px;color:#fff;font-size:2rem;background:none;border:0;cursor:pointer;line-height:1}
""").strip()


# ---------------------------------------------------------------------------
# FOOTER (společný)
# ---------------------------------------------------------------------------

def _footer_html(base: str = "") -> str:
    """base: '' pro index, '../' pro byt podstránku — aby odkazy fungovaly na GitHub Pages bez absolute paths."""
    index_link = f"{base}index.html" if base else ""
    return dedent(f"""
    <footer>
      <div class="wrap">
        <div>
          <h4>Dům Netušil</h4>
          <p>14 komorních bytů v historickém měšťanském domě<br>v centru Brna-Husovic.</p>
          <p>Netušilova 15, 614 00 Brno-Husovice</p>
        </div>
        <div>
          <h4>Navigace</h4>
          <ul>
            <li><a href="{index_link}#o-projektu">O projektu</a></li>
            <li><a href="{index_link}#byty">Byty</a></li>
            <li><a href="{index_link}#lokalita">Lokalita</a></li>
            <li><a href="{index_link}#galerie">Galerie</a></li>
            <li><a href="{index_link}#kontakt">Kontakt</a></li>
          </ul>
        </div>
        <div>
          <h4>Investor &amp; developer</h4>
          <p>BH projects &amp; development s.r.o.<br>Mezírka 775/1, Veveří, 602 00 Brno<br>IČ: 22340432 · DIČ: CZ22340432</p>
          <p>info@domnetusil.cz</p>
        </div>
        <div class="legal">
          © {date.today().year} BH projects &amp; development s.r.o. · Dům Netušil. Vizualizace jsou ilustrativní.
        </div>
      </div>
    </footer>
    """).strip()


# ---------------------------------------------------------------------------
# Šablona podstránky bytu
# ---------------------------------------------------------------------------

APT_PAGE_CSS = dedent("""
.hero-img{position:relative;height:70vh;min-height:520px;margin-top:72px;background-size:cover;background-position:center;overflow:hidden}
.hero-img::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.15) 0%,rgba(0,0,0,0) 30%,rgba(0,0,0,.65) 100%)}
.hero-img .label{position:absolute;bottom:30px;left:0;right:0;z-index:2;color:#fff}
.hero-img .label .wrap{display:flex;align-items:end;justify-content:space-between;gap:30px;flex-wrap:wrap}
.hero-img .label .breadcrumb{font-size:.72rem;text-transform:uppercase;letter-spacing:.22em;color:rgba(255,255,255,.85);margin-bottom:8px}
.hero-img .label h1{color:#fff;margin:0;font-weight:400;text-shadow:0 1px 4px rgba(0,0,0,.4)}
.hero-img .label h1 em{font-style:italic;color:#e4c792}
.hero-img .label .quick{display:flex;gap:32px}
.hero-img .label .quick div{text-align:right}
.hero-img .label .quick strong{display:block;font-family:var(--serif);font-size:1.8rem;font-weight:500;line-height:1;margin-bottom:4px}
.hero-img .label .quick span{font-size:.66rem;text-transform:uppercase;letter-spacing:.18em;color:rgba(255,255,255,.7)}
@media(max-width:760px){.hero-img{height:60vh}.hero-img .label .quick{display:none}}

.intro-strip{padding:48px 0;background:var(--paper);border-bottom:1px solid var(--line)}
.intro-strip .wrap{display:grid;grid-template-columns:1.3fr 1fr;gap:60px;align-items:center}
.intro-strip p{font-size:1.06rem;line-height:1.7;color:var(--ink-soft);margin:0}
.intro-strip .price-mini{text-align:right}
.intro-strip .price-mini .label{font-size:.66rem;text-transform:uppercase;letter-spacing:.2em;color:var(--ink-mute);margin-bottom:6px}
.intro-strip .price-mini .amount{font-family:var(--serif);font-size:2.2rem;color:var(--ink);font-weight:500;line-height:1}
.intro-strip .price-mini .sub{font-size:.78rem;color:var(--ink-mute);margin-top:4px}
@media(max-width:900px){.intro-strip .wrap{grid-template-columns:1fr;gap:24px}.intro-strip .price-mini{text-align:left}}

.gallery{padding:90px 0;background:var(--bg)}
.gallery .head{margin-bottom:48px}
.gallery .head h2{margin-bottom:8px}
.gallery .head p{max-width:600px;color:var(--ink-soft);margin:0}
.gallery .grid{display:grid;grid-template-columns:2fr 1fr;gap:20px;grid-template-areas:"big small1" "big small2"}
.gallery .item{position:relative;overflow:hidden;cursor:zoom-in;background:#ddd3c2;border:0}
.gallery .item.big{grid-area:big;min-height:560px}
.gallery .item.small1{grid-area:small1;min-height:270px}
.gallery .item.small2{grid-area:small2;min-height:270px}
.gallery .item img{width:100%;height:100%;object-fit:cover;transition:transform .6s}
.gallery .item:hover img{transform:scale(1.04)}
.gallery .item .caption{position:absolute;bottom:0;left:0;right:0;padding:18px 22px;color:#fff;background:linear-gradient(0deg,rgba(0,0,0,.7) 0%,rgba(0,0,0,0) 100%);font-family:var(--serif);font-size:1.1rem}
@media(max-width:900px){.gallery .grid{grid-template-columns:1fr;grid-template-areas:"big" "small1" "small2"}.gallery .item.big{min-height:340px}}

.detail{padding:100px 0}
.detail .grid{display:grid;grid-template-columns:1.4fr 1fr;gap:64px;align-items:start}
@media(max-width:1000px){.detail .grid{grid-template-columns:1fr;gap:40px}}
.info h2{margin-bottom:24px}
.info p{margin-bottom:1.4em;font-size:1.04rem;line-height:1.7}
.info .features{margin:36px 0;padding:28px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.info .features-title{font-family:var(--sans);font-size:.78rem;text-transform:uppercase;letter-spacing:.18em;color:var(--ink-mute);font-weight:600;margin-bottom:18px}
.info .features ul{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:14px 32px}
@media(max-width:600px){.info .features ul{grid-template-columns:1fr}}
.info .features li{padding-left:24px;position:relative;font-size:.95rem;color:var(--ink-soft)}
.info .features li::before{content:"";position:absolute;left:0;top:.6em;width:12px;height:1px;background:var(--accent)}
.info .specs{margin:36px 0}
.info .specs h3{font-size:.86rem;font-family:var(--sans);text-transform:uppercase;letter-spacing:.18em;font-weight:600;color:var(--ink-mute);margin-bottom:18px}
.info .specs table{width:100%;border-collapse:collapse;font-size:.92rem}
.info .specs td{padding:12px 0;border-bottom:1px solid var(--line);color:var(--ink-soft)}
.info .specs td:last-child{text-align:right;color:var(--ink);font-weight:500}
.info .specs tr.total td{border-top:2px solid var(--ink);border-bottom:0;padding-top:14px}
.info .specs tr.outdoor td{color:var(--ink-mute);font-style:italic;border-bottom:0;padding:6px 0}
.info .specs tr.outdoor td:last-child{color:var(--ink-mute)}

.floorplan{background:var(--paper);padding:32px;border:1px solid var(--line);position:sticky;top:96px}
.floorplan h3{font-size:.86rem;margin-bottom:16px;font-family:var(--sans);text-transform:uppercase;letter-spacing:.18em;font-weight:600;color:var(--ink-mute)}
.floorplan img{width:100%;height:auto;border:1px solid var(--line);cursor:zoom-in;transition:transform .2s}
.floorplan img:hover{transform:scale(1.02)}
.floorplan .download{display:inline-flex;align-items:center;gap:8px;margin-top:20px;font-size:.82rem;text-transform:uppercase;letter-spacing:.1em;font-weight:600;color:var(--accent-dark);border-bottom:1px solid var(--accent);padding-bottom:4px}

.bathroom{padding:100px 0;background:var(--paper);border-top:1px solid var(--line)}
.bathroom .grid{display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:center}
@media(max-width:900px){.bathroom .grid{grid-template-columns:1fr;gap:40px}}
.bathroom img{width:100%;height:auto;cursor:zoom-in;border:0}
.bathroom h2{margin-bottom:20px}
.bathroom ul{margin:24px 0;padding:0;list-style:none}
.bathroom li{padding:10px 0;border-bottom:1px solid var(--line);color:var(--ink-soft);display:flex;justify-content:space-between}
.bathroom li strong{color:var(--ink);font-weight:500}

.price-section{padding:90px 0;background:var(--ink);color:#fff}
.price-section .grid{display:grid;grid-template-columns:1.2fr 1fr;gap:60px;align-items:center}
@media(max-width:900px){.price-section .grid{grid-template-columns:1fr;gap:40px}}
.price-section .left h2{color:#fff;margin-bottom:16px}
.price-section .left p{color:rgba(255,255,255,.75);font-size:1.04rem;margin:0}
.price-section .left .eyebrow{color:#e4c792}
.price-section .price-card{background:rgba(255,255,255,.06);padding:36px;border:1px solid rgba(255,255,255,.12)}
.price-section .price-card .label{font-size:.72rem;text-transform:uppercase;letter-spacing:.22em;color:rgba(255,255,255,.6);margin-bottom:8px}
.price-section .price-card .amount{font-family:var(--serif);font-size:2.8rem;font-weight:500;line-height:1;margin-bottom:8px;color:#fff}
.price-section .price-card .sub{font-size:.88rem;color:rgba(255,255,255,.7);margin-bottom:28px}
.price-section .btn-accent{background:var(--accent);color:#fff;border-color:var(--accent);width:100%;justify-content:center;margin-bottom:10px;padding:18px 30px}
.price-section .btn-accent:hover{background:var(--accent-dark);border-color:var(--accent-dark)}
.price-section .btn-secondary{background:transparent;color:#fff;border:1px solid rgba(255,255,255,.4);width:100%;justify-content:center;padding:18px 30px}
.price-section .btn-secondary:hover{background:rgba(255,255,255,.1);border-color:#fff}
.price-section .small{display:block;margin-top:14px;font-size:.78rem;color:rgba(255,255,255,.5);text-align:center}

.next{padding:60px 0;background:var(--bg);border-top:1px solid var(--line)}
.next .wrap{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:24px}
.next .label{font-size:.72rem;text-transform:uppercase;letter-spacing:.22em;color:var(--ink-mute);margin-bottom:6px}
.next h3{font-family:var(--serif);font-size:1.6rem;font-weight:500;margin:0}
.next-btn{padding:14px 28px;background:var(--ink);color:#fff;font-weight:600;font-size:.84rem;letter-spacing:.06em;text-transform:uppercase;display:inline-flex;align-items:center;gap:10px;text-decoration:none;border:0}
.next-btn:hover{background:var(--accent-dark);color:#fff}

/* Status — hero stamp + price card */
.hero-img .status-stamp{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%) rotate(-10deg);z-index:3;color:#fff;font-family:var(--serif);font-size:4.5rem;font-weight:600;letter-spacing:.08em;padding:18px 56px;border:6px solid #fff;background:rgba(107,32,32,.94);text-shadow:0 2px 12px rgba(0,0,0,.4);pointer-events:none}
.hero-img .status-stamp-reserved{background:rgba(184,84,43,.94)}
.hero-img.status-prodano{filter:saturate(.7)}
.hero-img .breadcrumb .status-badge{display:inline-block;background:rgba(255,255,255,.95);padding:3px 10px;border-radius:999px;font-weight:700;letter-spacing:.08em;margin-left:6px}
.hero-img .breadcrumb .status-badge.status-k-dispozici{color:#3a7c4c}
.hero-img .breadcrumb .status-badge.status-rezervovano{color:#b8542b}
.hero-img .breadcrumb .status-badge.status-prodano{color:#6b2020}

.btn-disabled{pointer-events:none;opacity:.55;cursor:default}
.btn-disabled:hover{background:var(--accent);border-color:var(--accent)}

.price-card.status-card-rezervovano{border-color:rgba(184,84,43,.4);background:rgba(184,84,43,.08)}
.price-card.status-card-prodano{border-color:rgba(107,32,32,.4);background:rgba(107,32,32,.06)}
.price-card .amount-sold{text-decoration:line-through;color:rgba(255,255,255,.55)}
""").strip()


def render_apt_page(apt: dict) -> str:
    aid = apt["id"]
    plocha_str = _fmt_m2(apt["plocha"])
    cena_str = _fmt_kc(_calc_total_price(apt))
    cena_m2_str = _fmt_kc(apt["cena_kc_m2"])
    next_apt = next((a for a in APARTMENTS if a["id"] == apt["next_id"]), None)
    extra_text = apt["extra"]["popis"] if apt["extra"] else apt["patro"]

    # Status
    status = apt.get("status", "k dispozici")
    smeta = STATUS_META[status]
    status_label = smeta["label"]
    cta_text = smeta["cta_text"]
    cta_disabled = smeta["cta_disabled"]
    cta_href = "../index.html#kontakt" if not cta_disabled else "#"
    cta_class = "btn btn-accent" if not cta_disabled else "btn btn-accent btn-disabled"
    cta_aria = ' aria-disabled="true"' if cta_disabled else ""
    status_class = status.replace(" ", "-")  # "k dispozici" → "k-dispozici"
    sold_overlay = ""
    if status == "prodano":
        sold_overlay = '<div class="status-stamp">PRODÁNO</div>'
    elif status == "rezervovano":
        sold_overlay = '<div class="status-stamp status-stamp-reserved">REZERVOVÁNO</div>'

    # Rozdělit místnosti — interní (do součtu) vs venkovní (balkón/terasa pod součtem)
    internal_rooms = [(n, a) for n, a in apt["rooms"] if not any(k in n.lower() for k in ("balk", "teras"))]
    outdoor_rooms = [(n, a) for n, a in apt["rooms"] if any(k in n.lower() for k in ("balk", "teras"))]
    rooms_html = "\n          ".join(
        f"<tr><td>{_escape(name)}</td><td>{_escape(area)}</td></tr>"
        for name, area in internal_rooms
    )
    outdoor_html = "\n          ".join(
        f'<tr class="outdoor"><td>+ {_escape(name)}</td><td>{_escape(area)}</td></tr>'
        for name, area in outdoor_rooms
    )
    features_html = "\n            ".join(
        f"<li>{_escape(f)}</li>" for f in apt["features"]
    )

    title = f"Byt {aid} — {apt['dispozice']} {plocha_str} m² — Dům Netušil"
    description = apt["lead"][:155].rstrip(",.") + "."

    # JSON-LD strukturovaná data (Apartment + Offer)
    jsonld = {
        "@context": "https://schema.org",
        "@type": "Apartment",
        "name": f"Byt {aid} — {apt['headline']}",
        "description": apt["lead"],
        "numberOfRooms": 2 if "2+kk" in apt["dispozice"] else (3 if "3+kk" in apt["dispozice"] else 1),
        "floorSize": {"@type": "QuantitativeValue", "value": apt["plocha"], "unitCode": "MTK"},
        "floorLevel": apt["patro_short"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Netušilova 15",
            "addressLocality": "Brno-Husovice",
            "postalCode": "61400",
            "addressCountry": "CZ",
        },
        "offers": {
            "@type": "Offer",
            "price": _calc_total_price(apt),
            "priceCurrency": "CZK",
            "availability": "https://schema.org/InStock",
        },
    }

    return dedent(f"""\
<!doctype html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{_escape(description)}">
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<meta http-equiv="Referrer-Policy" content="strict-origin-when-cross-origin">
<meta http-equiv="X-Frame-Options" content="SAMEORIGIN">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'; font-src 'self'; base-uri 'self'; form-action 'self'; frame-ancestors 'self'">
<meta name="theme-color" content="#1b1b1b">
<meta name="robots" content="index,follow">
<link rel="canonical" href="{SITE_URL}/byty/byt-{aid}.html">

<!-- Open Graph -->
<meta property="og:type" content="product">
<meta property="og:title" content="{_escape(title)}">
<meta property="og:description" content="{_escape(description)}">
<meta property="og:url" content="{SITE_URL}/byty/byt-{aid}.html">
<meta property="og:image" content="{SITE_URL}/img/vizualizace/{apt['hero_img']}">
<meta property="og:locale" content="cs_CZ">

<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{_escape(title)}">
<meta name="twitter:description" content="{_escape(description)}">
<meta name="twitter:image" content="{SITE_URL}/img/vizualizace/{apt['hero_img']}">

<title>{_escape(title)}</title>

<link rel="preload" as="image" href="../img/vizualizace/{apt['hero_img']}">
<link rel="stylesheet" href="../styles.css">
</head>
<body>

<nav class="top">
  <div class="wrap">
    <a class="logo" href="../index.html">Dům Netušil<small>Netušilova 15 · Brno-Husovice</small></a>
    <a class="back" href="../index.html#byty">&larr; Zpět na byty</a>
  </div>
</nav>

<section class="hero-img status-{status_class}" id="hero" style="background-image:url('../img/vizualizace/{apt['hero_img']}')" role="img" aria-label="Vizualizace bytu {aid}">
  {sold_overlay}
  <div class="label">
    <div class="wrap">
      <div>
        <div class="breadcrumb">Byty · {_escape(apt['patro'])} · Byt {aid} · <span class="status-badge status-{status_class}">{status_label}</span></div>
        <h1>{apt['headline_html']}</h1>
      </div>
      <div class="quick">
        <div><strong>{plocha_str}&nbsp;m²</strong><span>Plocha</span></div>
        <div><strong>{_escape(apt['dispozice'])}</strong><span>Dispozice</span></div>
        <div><strong>{_escape(apt['patro_short'])}</strong><span>Patro</span></div>
      </div>
    </div>
  </div>
</section>

<section class="intro-strip">
  <div class="wrap">
    <p>{_escape(apt['lead'])}</p>
    <div class="price-mini">
      <div class="label">Kupní cena</div>
      <div class="amount">{cena_str}&nbsp;Kč</div>
      <div class="sub">{cena_m2_str} Kč/m² · vč. DPH</div>
    </div>
  </div>
</section>

<section class="gallery">
  <div class="wrap-wide">
    <div class="head">
      <span class="eyebrow">Vizualizace bytu</span>
      <h2>Jak bude byt vypadat.</h2>
      <p>Studio architektury 3D Atelier připravilo vizualizace interiéru — pro představu materiálů,
      rozložení a atmosféry. Skutečné provedení se může v detailech lišit.</p>
    </div>
    <div class="grid">
      <button class="item big" data-zoom><img src="../img/vizualizace/{apt['images'][0]}" alt="Obývací pokoj bytu {aid}" loading="lazy"><div class="caption">Obývací pokoj s kuchyňským koutem</div></button>
      <button class="item small1" data-zoom><img src="../img/vizualizace/{apt['images'][1]}" alt="Druhý pohled na byt {aid}" loading="lazy"><div class="caption">Detail interiéru</div></button>
      <button class="item small2" data-zoom><img src="../img/vizualizace/{apt['images'][2]}" alt="Pohled z exteriéru" loading="lazy"><div class="caption">Pohled z ulice</div></button>
    </div>
  </div>
</section>

<section class="detail" id="detaily">
  <div class="wrap">
    <div class="grid">
      <div class="info">
        <span class="eyebrow">O bytu</span>
        <h2>{_escape(apt['headline'])}</h2>
        {_description_html(apt['description'])}

        <div class="features">
          <div class="features-title">Co byt nabízí</div>
          <ul>
            {features_html}
          </ul>
        </div>

        <div class="specs">
          <h3>Plochy místností</h3>
          <table>
          {rooms_html}
          <tr class="total"><td><strong>Celkem užitná plocha</strong></td><td><strong>{plocha_str}&nbsp;m²</strong></td></tr>
          {outdoor_html}
          </table>
        </div>

        <div class="specs">
          <h3>Technické parametry</h3>
          <table>
            <tr><td>Vytápění</td><td>Tepelné čerpadlo</td></tr>
            <tr><td>Energetická třída</td><td>B (úsporná)</td></tr>
            <tr><td>Konstrukce stěn</td><td>Cihelné tvarovky HELUZ</td></tr>
            <tr><td>Zateplení</td><td>Minerální vata</td></tr>
            <tr><td>Patro</td><td>{_escape(apt['patro'])}</td></tr>
            <tr><td>Stav</td><td>Volný k jednání</td></tr>
            <tr><td>Předání</td><td>Q4 2026</td></tr>
          </table>
        </div>
      </div>

      <aside class="floorplan">
        <h3>Půdorys bytu</h3>
        <img src="../img/pudorysy/byt-{aid}.png" alt="Půdorys bytu {aid}" data-zoom loading="lazy">
        <a href="../img/pudorysy/byt-{aid}.png" download class="download" rel="noopener">⤓ Stáhnout půdorys</a>
      </aside>
    </div>
  </div>
</section>

<section class="bathroom">
  <div class="wrap">
    <div class="grid">
      <div>
        <img src="../img/vizualizace/koupelna.jpg" alt="Vzorová koupelna" data-zoom loading="lazy">
      </div>
      <div>
        <span class="eyebrow">Vzorová koupelna</span>
        <h2>Vana, designové dlažby, přírodní materiály.</h2>
        <p>Všechny byty v Domě Netušil mají koupelny v jednotném standardu — kvalitní obklady,
        kvalitní sanita, baterie Hansgrohe. Možnost dovybavení dle individuálního výběru klienta.</p>
        <ul>
          <li><span>Vana</span><strong>Standard</strong></li>
          <li><span>WC kompletní</span><strong>Geberit</strong></li>
          <li><span>Obklady</span><strong>Velkoformátový gres</strong></li>
          <li><span>Podlahové vytápění</span><strong>Ano</strong></li>
          <li><span>Odvětrání</span><strong>Centrální VZT</strong></li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="price-section">
  <div class="wrap">
    <div class="grid">
      <div class="left">
        <span class="eyebrow">{
            'Připraveno k jednání' if status == 'k dispozici'
            else 'Rezervováno' if status == 'rezervovano'
            else 'Prodáno'
        }</span>
        <h2>{
            'Tento byt je k dispozici.' if status == 'k dispozici'
            else 'Tento byt je rezervován.' if status == 'rezervovano'
            else 'Tento byt je prodán.'
        }</h2>
        <p>{
            'Ozvete se nám pro rezervaci, prohlídku nebo individuální nabídku. Pro předplatitele (předplacení 50–70 % kupní ceny) je k dispozici výhodnější cena. Odpovídáme do 24 hodin.' if status == 'k dispozici'
            else 'Tento byt je momentálně rezervován. Můžete si nechat zaslat upozornění, pokud by se status změnil — případně se podívejte na podobné dostupné byty.' if status == 'rezervovano'
            else 'Tento byt byl prodán. Pokud Vás zajímají podobné dispozice v Domě Netušil, podívejte se na ostatní byty.'
        }</p>
      </div>
      <div class="price-card status-card-{status_class}">
        <div class="label">{
            'Kupní cena (vč. DPH)' if status != 'prodano' else 'Prodejní cena (vč. DPH)'
        }</div>
        <div class="amount {'amount-sold' if status == 'prodano' else ''}">{cena_str}&nbsp;Kč</div>
        <div class="sub">{cena_m2_str} Kč/m²{' · Výhodnější cena pro předplatitele (50–70 % kupní ceny)' if status == 'k dispozici' else ''}</div>
        <a class="{cta_class}" href="{cta_href}"{cta_aria}>{cta_text}</a>
        <a class="btn btn-secondary" href="../img/pudorysy/byt-{aid}.png" download>Stáhnout půdorys</a>
        <span class="small">{
            'Odpovídáme do 24 hodin · BH projects &amp; development s.r.o.' if status == 'k dispozici'
            else 'Pro dotazy: info@domnetusil.cz'
        }</span>
      </div>
    </div>
  </div>
</section>

<section class="next">
  <div class="wrap">
    <div>
      <div class="label">Pokračovat na další byt</div>
      <h3>Byt {next_apt['id']} · {_escape(next_apt['headline'])}</h3>
    </div>
    <a href="byt-{next_apt['id']}.html" class="next-btn">Zobrazit &rarr;</a>
  </div>
</section>

{_footer_html(base="../")}

<div class="lightbox" id="lightbox">
  <button class="close" aria-label="Zavřít">×</button>
  <img id="lightboxImg" src="" alt="">
</div>

<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False, indent=2)}</script>
<script src="../script.js" defer></script>
</body>
</html>
""")


# ---------------------------------------------------------------------------
# HLAVNÍ STRÁNKA (index.html)
# ---------------------------------------------------------------------------

INDEX_CSS = dedent("""
.hero{position:relative;min-height:100vh;display:flex;align-items:flex-end;color:#fff;overflow:hidden}
.hero-bg{position:absolute;inset:0;background-image:url('img/vizualizace/ext-1.jpg');background-size:cover;background-position:center;transform:scale(1.05)}
.hero::before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.35) 0%,rgba(0,0,0,.15) 35%,rgba(0,0,0,.55) 75%,rgba(0,0,0,.88) 100%);z-index:1}
.hero .inner{position:relative;z-index:2;width:100%;padding:180px 0 90px}
.hero .eyebrow{color:#e4c792}
.hero h1{color:#fff;max-width:960px;font-weight:400}
.hero h1 em{font-style:italic;color:#e4c792}
.hero p.lead{max-width:680px;color:rgba(255,255,255,.9);font-size:1.16rem;margin:20px 0 42px;line-height:1.65}
.hero .cta{display:flex;gap:16px;flex-wrap:wrap}
.hero .facts{display:grid;grid-template-columns:repeat(4,1fr);gap:36px;margin-top:80px;padding-top:40px;border-top:1px solid rgba(255,255,255,.22)}
.hero .facts div strong{display:block;font-family:var(--serif);font-size:1.9rem;color:#fff;font-weight:500;margin-bottom:6px;line-height:1}
.hero .facts div span{font-size:.72rem;text-transform:uppercase;letter-spacing:.18em;color:rgba(255,255,255,.72)}
@media(max-width:760px){.hero .facts{grid-template-columns:repeat(2,1fr);gap:24px}}

section{padding:120px 0;position:relative}
@media(max-width:760px){section{padding:70px 0}}

.apts{background:var(--bg)}
.apts .head{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:end;margin-bottom:60px}
.apts .head p{margin:0;max-width:520px;color:var(--ink-soft);font-size:1.02rem}
@media(max-width:900px){.apts .head{grid-template-columns:1fr;gap:24px}}
.apts .filter{display:flex;gap:14px;margin-bottom:40px;flex-wrap:wrap}
.apts .filter button{background:transparent;border:1px solid var(--line);padding:10px 20px;font-size:.82rem;text-transform:uppercase;letter-spacing:.1em;font-weight:600;cursor:pointer;color:var(--ink-soft);font-family:var(--sans)}
.apts .filter button.active{background:var(--ink);color:#fff;border-color:var(--ink)}
.apts .filter button:hover{border-color:var(--ink)}
.apts .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:32px}
@media(max-width:1000px){.apts .grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:680px){.apts .grid{grid-template-columns:1fr}}

.card-apt{position:relative;background:var(--paper);border:1px solid var(--line);cursor:pointer;text-decoration:none;color:inherit;display:block;transition:transform .3s,box-shadow .3s}
.card-apt:hover{transform:translateY(-6px);box-shadow:0 24px 50px rgba(0,0,0,.08);border-color:var(--accent)}
.card-apt .thumb{height:240px;background-size:cover;background-position:center;position:relative}
.card-apt .tag{position:absolute;top:18px;left:18px;background:rgba(0,0,0,.7);color:#fff;font-size:.7rem;padding:6px 12px;text-transform:uppercase;letter-spacing:.12em;font-weight:600;z-index:2}
.card-apt .nr-patro{position:absolute;bottom:18px;left:18px;color:#fff;font-family:var(--serif);font-size:1rem;letter-spacing:.04em;text-shadow:0 1px 4px rgba(0,0,0,.7);z-index:2}
.card-apt .body{padding:26px 24px 28px}
.card-apt h3{font-family:var(--serif);font-weight:500;font-size:1.35rem;margin:0 0 12px;line-height:1.2}
.card-apt .meta{display:flex;gap:14px;font-size:.8rem;color:var(--ink-mute);margin-bottom:14px;flex-wrap:wrap}
.card-apt .meta span{position:relative}
.card-apt .meta span:not(:last-child)::after{content:"·";position:absolute;right:-10px;color:var(--line)}
.card-apt .desc{font-size:.9rem;color:var(--ink-soft);margin:0 0 18px;line-height:1.6}
.card-apt .foot{display:flex;justify-content:space-between;align-items:center;padding-top:18px;border-top:1px solid var(--line)}
.card-apt .price-value{font-family:var(--serif);font-size:1.3rem;color:var(--ink);font-weight:500;display:block;line-height:1}
.card-apt .price-sub{font-size:.68rem;color:var(--ink-mute);text-transform:uppercase;letter-spacing:.1em;margin-top:4px;display:block}
.card-apt .arrow{font-size:1.4rem;color:var(--accent-dark)}

/* Status — badge + overlay na kartách */
.status-badge{position:absolute;top:18px;right:18px;background:rgba(255,255,255,.95);font-size:.65rem;padding:5px 11px;text-transform:uppercase;letter-spacing:.12em;font-weight:700;z-index:3;border-radius:999px}
.status-badge.status-k-dispozici{color:#3a7c4c}
.status-badge.status-rezervovano{color:#b8542b}
.status-badge.status-prodano{color:#6b2020}

.card-apt.status-rezervovano .thumb{filter:saturate(.85)}
.card-apt.status-prodano .thumb{filter:grayscale(.8) brightness(.85)}
.card-apt.status-prodano .body{opacity:.6}
.card-apt.status-prodano .price-value{text-decoration:line-through;color:var(--ink-mute)}
.card-apt.status-prodano:hover{transform:none;box-shadow:none;border-color:var(--line);cursor:default}
.card-apt.status-rezervovano:hover{transform:translateY(-3px)}

.card-stamp{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%) rotate(-12deg);z-index:5;color:#fff;font-family:var(--serif);font-size:2.6rem;font-weight:600;letter-spacing:.08em;padding:14px 36px;border:4px solid #fff;background:rgba(107,32,32,.92);text-shadow:0 2px 8px rgba(0,0,0,.35);pointer-events:none}
.card-stamp.card-stamp-reserved{background:rgba(184,84,43,.92)}

/* Filtr status */
.filter-status{margin-top:0;margin-bottom:40px}
.filter-status button[data-filter-status="k-dispozici"].active{background:#3a7c4c;color:#fff;border-color:#3a7c4c}
.filter-status button[data-filter-status="rezervovano"].active{background:#b8542b;color:#fff;border-color:#b8542b}
.filter-status button[data-filter-status="prodano"].active{background:#6b2020;color:#fff;border-color:#6b2020}
""").strip()


def render_index(apartments: list[dict]) -> str:
    # Spočítat počty
    total_count = len(apartments)
    count_1kk = sum(1 for a in apartments if a["dispozice"].startswith("1+kk"))
    count_2kk = sum(1 for a in apartments if a["dispozice"].startswith("2+kk"))
    count_3kk = sum(1 for a in apartments if a["dispozice"].startswith("3+kk"))
    count_avail = sum(1 for a in apartments if a.get("status", "k dispozici") == "k dispozici")
    count_reserved = sum(1 for a in apartments if a.get("status") == "rezervovano")
    count_sold = sum(1 for a in apartments if a.get("status") == "prodano")

    cards_html = []
    for apt in apartments:
        cena = _fmt_kc(_calc_total_price(apt))
        extra = apt["extra"]["popis"] if apt["extra"] else apt["patro_short"]
        status = apt.get("status", "k dispozici")
        status_class = status.replace(" ", "-")
        smeta = STATUS_META[status]
        status_label = smeta["label"]
        # Status overlay (sold/reserved)
        status_overlay = ""
        if status == "prodano":
            status_overlay = '<div class="card-stamp">PRODÁNO</div>'
        elif status == "rezervovano":
            status_overlay = '<div class="card-stamp card-stamp-reserved">REZERVOVÁNO</div>'

        cards_html.append(dedent(f"""
        <a class="card-apt status-{status_class}" href="byty/byt-{apt['id']}.html"
           data-dispozice="{_escape(apt['dispozice'])}"
           data-patro="{_escape(apt['patro_short'])}"
           data-status="{status_class}">
          {status_overlay}
          <div class="thumb" style="background-image:linear-gradient(180deg,rgba(0,0,0,0.05) 0%,rgba(0,0,0,0.45) 100%),url('img/vizualizace/{apt['hero_img']}')">
            <span class="tag">{_escape(apt['tag'])}</span>
            <span class="status-badge status-{status_class}">{status_label}</span>
            <span class="nr-patro">Byt {apt['id']} · {_escape(apt['patro'])}</span>
          </div>
          <div class="body">
            <h3>{_escape(apt['headline'])}</h3>
            <div class="meta">
              <span>{_fmt_m2(apt['plocha'])} m²</span>
              <span>{_escape(apt['dispozice'])}</span>
              <span>{_escape(extra)}</span>
            </div>
            <p class="desc">{_escape(apt['lead'][:120])}…</p>
            <div class="foot">
              <div><span class="price-value">{cena}&nbsp;Kč</span><span class="price-sub">vč. DPH</span></div>
              <div class="arrow" aria-hidden="true">&rarr;</div>
            </div>
          </div>
        </a>
        """).strip())

    return dedent(f"""\
<!doctype html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Dům Netušil — 14 komorních bytů 1+kk, 2+kk a 3+kk v historickém měšťanském domě v centru Brna-Husovic. Zdobná fasáda, tepelné čerpadlo, zelená střecha. Předání Q4 2026.">
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<meta http-equiv="Referrer-Policy" content="strict-origin-when-cross-origin">
<meta http-equiv="X-Frame-Options" content="SAMEORIGIN">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'; font-src 'self'; base-uri 'self'; form-action 'self'; frame-ancestors 'self'">
<meta name="theme-color" content="#1b1b1b">
<meta name="robots" content="index,follow">
<link rel="canonical" href="{SITE_URL}/">

<meta property="og:type" content="website">
<meta property="og:title" content="Dům Netušil — 14 komorních bytů v centru Brna-Husovic">
<meta property="og:description" content="Nové byty 1+kk, 2+kk a 3+kk v historickém měšťanském domě. Zdobná fasáda, tepelné čerpadlo, zelená střecha.">
<meta property="og:url" content="{SITE_URL}/">
<meta property="og:image" content="{SITE_URL}/img/vizualizace/ext-1.jpg">
<meta property="og:locale" content="cs_CZ">

<title>Dům Netušil — 14 komorních bytů v historickém domě Brno-Husovice</title>
<link rel="preload" as="image" href="img/vizualizace/ext-1.jpg">
<link rel="stylesheet" href="styles.css">
</head>
<body>

<nav class="top">
  <div class="wrap">
    <a class="logo" href="#">Dům Netušil<small>Netušilova 15 · Brno-Husovice</small></a>
    <ul>
      <li><a href="#o-projektu">O projektu</a></li>
      <li><a href="#byty">Byty</a></li>
      <li><a href="#lokalita">Lokalita</a></li>
      <li><a href="#galerie">Galerie</a></li>
    </ul>
    <a class="btn btn-outline" href="#kontakt">Mám zájem</a>
  </div>
</nav>

<header class="hero">
  <div class="hero-bg" role="img" aria-label="Pohled na historický dům Netušilova 15"></div>
  <div class="wrap inner">
    <span class="eyebrow">Netušilova 15 · Brno-Husovice</span>
    <h1>Husovice,<br>jak je <em>ještě neznáte</em>.</h1>
    <p class="lead">Čtrnáct komorních bytů 1+kk, 2+kk a 3+kk v historickém měšťanském domě
    v srdci Brna-Husovic. Zdobná fasáda z konce 19. století.
    Nové interiéry, tepelné čerpadlo, zelená střecha. Deset minut tramvají do centra.</p>
    <div class="cta">
      <a class="btn btn-primary" href="#byty">Prohlédnout byty</a>
      <a class="btn btn-ghost" href="#kontakt">Zjistit cenu</a>
    </div>
    <div class="facts">
      <div><strong>14</strong><span>Bytů 1+kk, 2+kk a 3+kk</span></div>
      <div><strong>24–60 m²</strong><span>Výměra jednotek</span></div>
      <div><strong>Památková zóna</strong><span>Historická fasáda</span></div>
      <div><strong>Únor 2027</strong><span>Plánované dokončení</span></div>
    </div>
  </div>
</header>

<section class="apts" id="byty">
  <div class="wrap">
    <div class="head">
      <div>
        <span class="eyebrow">Výběr bytů</span>
        <h2>14 bytů. 14 různých příběhů.</h2>
      </div>
      <p>Vyberte si podle velikosti, patra nebo vybavení. Každý byt v Domě Netušil
      má něco svého — od kompaktních 1+kk až po podkrovní 3+kk.</p>
    </div>

    <div class="filter" role="group" aria-label="Filtr podle dispozice">
      <button data-filter-disp="all" class="active">Všechny ({total_count})</button>
      <button data-filter-disp="1+kk">1+kk ({count_1kk})</button>
      <button data-filter-disp="2+kk">2+kk ({count_2kk})</button>
      <button data-filter-disp="3+kk">3+kk ({count_3kk})</button>
    </div>

    <div class="filter filter-status" role="group" aria-label="Filtr podle dostupnosti">
      <button data-filter-status="all" class="active">Vše ({total_count})</button>
      <button data-filter-status="k-dispozici">Volné ({count_avail})</button>
      <button data-filter-status="rezervovano">Rezervované ({count_reserved})</button>
      <button data-filter-status="prodano">Prodané ({count_sold})</button>
    </div>

    <div class="grid" id="aptsGrid">
      {chr(10).join(cards_html)}
    </div>
  </div>
</section>

{_footer_html()}

<script src="script.js" defer></script>
</body>
</html>
""")


# ---------------------------------------------------------------------------
# Sdílený JS (filtrování + lightbox)
# ---------------------------------------------------------------------------

SHARED_JS = dedent("""
(() => {
  'use strict';

  // Lightbox pro [data-zoom] obrázky
  const lb = document.getElementById('lightbox');
  if (lb) {
    const lbImg = document.getElementById('lightboxImg');
    const lbClose = lb.querySelector('.close');

    const open = (src, alt) => {
      lbImg.src = src;
      lbImg.alt = alt || '';
      lb.classList.add('open');
      document.body.style.overflow = 'hidden';
    };
    const close = () => {
      lb.classList.remove('open');
      document.body.style.overflow = '';
      setTimeout(() => { lbImg.src = ''; }, 250);
    };

    document.querySelectorAll('[data-zoom]').forEach(el => {
      el.addEventListener('click', (e) => {
        e.preventDefault();
        const img = el.tagName === 'IMG' ? el : el.querySelector('img');
        if (img) open(img.src, img.alt);
      });
    });

    lb.addEventListener('click', (e) => {
      if (e.target === lb || e.target === lbImg) close();
    });
    if (lbClose) lbClose.addEventListener('click', close);
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && lb.classList.contains('open')) close();
    });
  }

  // Filtry bytů na hlavní stránce (dispozice + status)
  const grid = document.getElementById('aptsGrid');
  const state = { disp: 'all', status: 'all' };

  const apply = () => {
    if (!grid) return;
    grid.querySelectorAll('.card-apt').forEach(card => {
      const disp = card.dataset.dispozice || '';
      const status = card.dataset.status || '';
      const dispOk = (state.disp === 'all' || disp.startsWith(state.disp));
      const statusOk = (state.status === 'all' || status === state.status);
      card.style.display = (dispOk && statusOk) ? '' : 'none';
    });
  };

  const setupFilter = (selector, key) => {
    const buttons = document.querySelectorAll(selector + ' button');
    buttons.forEach(btn => {
      btn.addEventListener('click', () => {
        state[key] = btn.dataset['filter' + key.charAt(0).toUpperCase() + key.slice(1)];
        buttons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        apply();
      });
    });
  };

  setupFilter('.apts .filter:not(.filter-status)', 'disp');
  setupFilter('.apts .filter-status', 'status');
})();
""").strip()


# ---------------------------------------------------------------------------
# sitemap.xml a robots.txt
# ---------------------------------------------------------------------------

def render_sitemap() -> str:
    today = date.today().isoformat()
    urls = [f"  <url><loc>{SITE_URL}/</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>1.0</priority></url>"]
    for apt in APARTMENTS:
        urls.append(f"  <url><loc>{SITE_URL}/byty/byt-{apt['id']}.html</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>")
    return dedent(f"""\
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>
""")


def render_robots() -> str:
    return dedent(f"""\
User-agent: *
Allow: /
Disallow: /generate.py
Disallow: /*.md

Sitemap: {SITE_URL}/sitemap.xml
""")


def render_404() -> str:
    """Custom 404 stránka — funguje jako index pro GitHub Pages i Apache."""
    return dedent(f"""\
<!doctype html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<meta name="robots" content="noindex">
<title>Stránka nenalezena — Dům Netušil</title>
<link rel="stylesheet" href="/styles.css">
<style>
  body{{display:flex;align-items:center;justify-content:center;min-height:100vh;background:var(--bg)}}
  .err{{text-align:center;max-width:560px;padding:40px}}
  .err h1{{font-size:6rem;color:var(--accent);margin:0 0 10px;font-weight:300}}
  .err h2{{margin:0 0 20px}}
  .err p{{margin-bottom:30px;color:var(--ink-soft)}}
</style>
</head>
<body>
<div class="err">
  <h1>404</h1>
  <h2>Tady to není.</h2>
  <p>Stránka, kterou hledáte, neexistuje nebo byla přesunuta. Vraťte se na úvod
  a najděte si svůj nový byt v Domě Netušil.</p>
  <a class="btn btn-primary" href="/">Zpět na úvod</a>
</div>
</body>
</html>
""")


def render_htaccess() -> str:
    return dedent("""\
# Security headers
<IfModule mod_headers.c>
  Header always set X-Content-Type-Options "nosniff"
  Header always set X-Frame-Options "SAMEORIGIN"
  Header always set Referrer-Policy "strict-origin-when-cross-origin"
  Header always set Permissions-Policy "geolocation=(), microphone=(), camera=()"
  Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains" env=HTTPS
</IfModule>

# Cache obrázků a statiky
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/png "access plus 30 days"
  ExpiresByType image/jpeg "access plus 30 days"
  ExpiresByType image/webp "access plus 30 days"
  ExpiresByType text/css "access plus 7 days"
  ExpiresByType application/javascript "access plus 7 days"
</IfModule>

# Gzip komprese
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript application/json image/svg+xml
</IfModule>

# Friendly URLs pro byty: /byt-01 → /byty/byt-01.html
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^byt-(\\d{2})/?$ byty/byt-$1.html [L]

# Vlastní 404
ErrorDocument 404 /404.html

# Blokovat přístup ke generátoru a md
<FilesMatch "\\.(py|md|log)$">
  Require all denied
</FilesMatch>

# Force HTTPS (závisí na hostingu)
# RewriteCond %{HTTPS} off
# RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
""")


# ---------------------------------------------------------------------------
# Generování
# ---------------------------------------------------------------------------

def main():
    root = Path(__file__).parent
    byty_dir = root / "byty"
    byty_dir.mkdir(exist_ok=True)

    # Načíst ceny z ceny.json a injektovat do APARTMENTS
    ceny = load_ceny()
    for apt in APARTMENTS:
        cena_info = ceny[apt["id"]]
        apt["cena_kc"] = cena_info["cena_kc"]
        apt["cena_kc_m2"] = cena_info["cena_kc_m2"]
        apt["cena_terasy_kc"] = cena_info.get("cena_terasy_kc")
        apt["cena_balkonu_kc"] = cena_info.get("cena_balkonu_kc")

    # Načíst statusy a injektovat je do APARTMENTS
    statuses = load_statuses()
    for apt in APARTMENTS:
        info = statuses.get(apt["id"], {"status": "k dispozici"})
        apt["status"] = info.get("status", "k dispozici")
        apt["status_poznamka"] = info.get("poznamka", "")

    # styles.css
    css = SHARED_CSS + "\n\n/* index */\n" + INDEX_CSS + "\n\n/* apt page */\n" + APT_PAGE_CSS
    (root / "styles.css").write_text(css)

    # script.js
    (root / "script.js").write_text(SHARED_JS)

    # 14 podstránek
    for apt in APARTMENTS:
        (byty_dir / f"byt-{apt['id']}.html").write_text(render_apt_page(apt))

    # index.html
    (root / "index.html").write_text(render_index(APARTMENTS))

    # sitemap, robots, .htaccess
    (root / "sitemap.xml").write_text(render_sitemap())
    (root / "robots.txt").write_text(render_robots())
    (root / ".htaccess").write_text(render_htaccess())

    # GitHub Pages soubory
    (root / "404.html").write_text(render_404())
    (root / ".nojekyll").write_text("")  # Vypne Jekyll processing
    if not (root / "CNAME").exists():
        (root / "CNAME").write_text("dumnetusil.cz\n")
    # Poznámka: .github/workflows/ NEGENERUJEME — náš workflow je
    # "edit v chatu → push hotovou verzi na Git", ne CI/CD.

    # Souhrn statusů
    avail = sum(1 for a in APARTMENTS if a["status"] == "k dispozici")
    reserved = sum(1 for a in APARTMENTS if a["status"] == "rezervovano")
    sold = sum(1 for a in APARTMENTS if a["status"] == "prodano")

    print(f"✓ Generováno {len(APARTMENTS)} podstránek + index + sitemap + robots + .htaccess + 404.html + .nojekyll")
    print(f"  Status: {avail} k dispozici · {reserved} rezervováno · {sold} prodáno")


if __name__ == "__main__":
    main()
