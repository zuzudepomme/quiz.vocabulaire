#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère mots.json à partir du dictionnaire du français difficile de webnext.fr.

Dépendances : pip install requests beautifulsoup4

Utilisation :
    python build_data.py            -> scrape tout et écrit mots.json
    python build_data.py --pages 10 -> ne scrape que les 10 premières pages (test rapide)

Une fois mots.json généré, commite-le et pushe-le : le site (index.html)
le charge automatiquement au chargement de la page.
"""

import json
import re
import sys
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup, NavigableString

BASE_URL = "https://webnext.fr/dictionnaire-du-francais-difficile-mots-rares-et-recherches-1016.html"
NB_PAGES_TOTAL = 72
OUTPUT_FILE = Path(__file__).with_name("mots.json")
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; QuizMotsRares/1.0)"}


def fetch_page(page_num: int) -> str:
    params = {} if page_num == 1 else {"page_num": page_num}
    resp = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return resp.text


def extract_block_text(h2_tag) -> str:
    parts = []
    for el in h2_tag.next_elements:
        if getattr(el, "name", None) == "h2":
            break
        if isinstance(el, NavigableString):
            text = str(el).strip()
            if text:
                parts.append(text)
    return " ".join(parts)


def clean_definition(word: str, raw_text: str) -> str:
    main_part = raw_text.split("«")[0]
    main_part = re.sub(r"\s+", " ", main_part).strip()
    main_part = main_part.lstrip(":-— ").strip()
    if main_part.lower().startswith(word.lower()):
        main_part = main_part[len(word):].strip()
        main_part = main_part.lstrip(":-— ").strip()
    return main_part


def extract_citations(raw_text: str):
    citations = re.findall(r"«\s*(.*?)\s*»", raw_text, flags=re.DOTALL)
    return [re.sub(r"\s+", " ", c).strip() for c in citations if c.strip()]


def parse_page(html: str):
    soup = BeautifulSoup(html, "html.parser")
    entries = []
    for h2 in soup.find_all("h2"):
        link = h2.find("a", href=lambda h: h and "definition-du-mot" in h)
        if not link:
            continue
        word = link.get_text(strip=True)
        url = link["href"]
        raw = extract_block_text(h2)
        definition = clean_definition(word, raw)
        citations = extract_citations(raw)
        if word and definition and len(definition) > 5:
            entries.append({"mot": word, "definition": definition, "citations": citations, "url": url})
    return entries


def scrape_all_pages(nb_pages: int):
    all_entries = []
    seen = set()
    for page_num in range(1, nb_pages + 1):
        print(f"\rPage {page_num}/{nb_pages}...", end="", flush=True)
        try:
            html = fetch_page(page_num)
        except requests.RequestException as e:
            print(f"\nErreur page {page_num} : {e}")
            continue
        for entry in parse_page(html):
            if entry["mot"] not in seen:
                seen.add(entry["mot"])
                all_entries.append(entry)
        time.sleep(0.3)
    print(f"\r{len(all_entries)} mots récupérés.{' ' * 20}")
    return all_entries


def main():
    nb_pages = NB_PAGES_TOTAL
    if "--pages" in sys.argv:
        nb_pages = int(sys.argv[sys.argv.index("--pages") + 1])

    entries = scrape_all_pages(nb_pages)
    OUTPUT_FILE.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Écrit dans {OUTPUT_FILE.name} ({len(entries)} mots).")


if __name__ == "__main__":
    main()
