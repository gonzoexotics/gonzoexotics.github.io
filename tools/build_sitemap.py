from __future__ import annotations

from html import unescape
from pathlib import Path
from urllib.parse import urljoin, urlsplit
from xml.etree.ElementTree import Element, SubElement, indent, tostring
import re


ROOT = Path(__file__).resolve().parents[1]
BASE = "https://gonzoexotics.github.io/"
LASTMOD = "2026-08-22"

PAGES = [
    "index.html",
    "morelia-viridis.html",
    "corallus-caninus.html",
    "python-bivittatus.html",
    "hodowla-python-bivittatus-2026.html",
    "baza-wiedzy.html",
    "galeria.html",
    "baza-wiedzy/corallus-batesii-marzenie-terrarysty.html",
    "baza-wiedzy/corallus-caninus-sezonowosc-wilgotnosc-zraszanie.html",
    "baza-wiedzy/jak-kupic-zdrowego-pytona-zielonego-corallus-caninus.html",
    "baza-wiedzy/morelia-viridis-zmiana-koloru-neonaty-dorosle.html",
    "baza-wiedzy/python-bivittatus-genetyka-morphy-odmiany-barwne.html",
    "baza-wiedzy/python-bivittatus-zywienie-tempo-wzrostu-kondycja.html",
    "baza-wiedzy/pyton-zielony-lokalizacje-morelia-viridis-azurea.html",
    "baza-wiedzy/surykatka-w-domu-tofik-opieka-zachowanie-zywienie.html",
]


def first(pattern: str, source: str) -> str:
    match = re.search(pattern, source, flags=re.I | re.S)
    return unescape(match.group(1).strip()) if match else ""


def page_url(relative: str) -> str:
    return BASE if relative == "index.html" else urljoin(BASE, relative.replace("\\", "/"))


urlset = Element(
    "urlset",
    {
        "xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9",
        "xmlns:image": "http://www.google.com/schemas/sitemap-image/1.1",
    },
)

image_count = 0

for relative in PAGES:
    source = (ROOT / relative).read_text(encoding="utf-8")
    canonical = first(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)', source)
    title = first(r"<title>(.*?)</title>", source)
    image_sources: list[str] = []
    for image_src in re.findall(r'<img\b[^>]+src=["\']([^"\']+)', source, flags=re.I | re.S):
        absolute = urljoin(page_url(relative), unescape(image_src.strip()))
        if urlsplit(absolute).netloc == urlsplit(BASE).netloc and absolute not in image_sources:
            image_sources.append(absolute)

    og_image = first(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)', source)
    if og_image:
        absolute_og = urljoin(page_url(relative), og_image)
        if urlsplit(absolute_og).netloc == urlsplit(BASE).netloc and absolute_og not in image_sources:
            image_sources.insert(0, absolute_og)

    url = SubElement(urlset, "url")
    SubElement(url, "loc").text = canonical or page_url(relative)
    SubElement(url, "lastmod").text = LASTMOD

    for image_src in image_sources[:1000]:
        image = SubElement(url, "image:image")
        SubElement(image, "image:loc").text = image_src
        image_count += 1

indent(urlset, space="  ")
xml = '<?xml version="1.0" encoding="UTF-8"?>\n' + tostring(urlset, encoding="unicode") + "\n"
(ROOT / "sitemap.xml").write_text(xml, encoding="utf-8", newline="\n")
print(f"Built sitemap.xml with {len(PAGES)} URLs and {image_count} image entries")
