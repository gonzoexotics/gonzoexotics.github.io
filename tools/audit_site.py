from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree
import json
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
EXEMPT_PREFIXES = ("google",)


class Parser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.images: list[dict[str, str | None]] = []
        self.links: list[str] = []
        self.h1 = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "img" and values.get("src"):
            self.images.append(values)
        elif tag == "a" and values.get("href"):
            self.links.append(values["href"] or "")
        elif tag == "h1":
            self.h1 += 1


def local_target(page: Path, value: str) -> Path | None:
    value = unquote(value.split("#", 1)[0].split("?", 1)[0])
    if not value or value.startswith(("http://", "https://", "mailto:", "tel:", "javascript:", "data:")):
        return None
    target = ROOT / value.lstrip("/") if value.startswith("/") else page.parent / value
    if value.endswith("/"):
        target /= "index.html"
    return target.resolve()


errors: list[str] = []
html_files = sorted(ROOT.rglob("*.html"))

for page in html_files:
    if any(part in {".git", "tools"} for part in page.parts) or page.name.startswith(EXEMPT_PREFIXES):
        continue
    source = page.read_text(encoding="utf-8")
    rel = page.relative_to(ROOT).as_posix()
    parser = Parser()
    parser.feed(source)

    required = {
        "title": r"<title>.+?</title>",
        "description": r'<meta[^>]+name=["\']description["\']',
        "canonical": r'<link[^>]+rel=["\']canonical["\']',
        "robots": r'<meta[^>]+name=["\']robots["\'][^>]+max-image-preview:large',
        "og:title": r'<meta[^>]+property=["\']og:title["\']',
        "og:description": r'<meta[^>]+property=["\']og:description["\']',
        "og:url": r'<meta[^>]+property=["\']og:url["\']',
        "og:image": r'<meta[^>]+property=["\']og:image["\']',
        "twitter:card": r'<meta[^>]+name=["\']twitter:card["\']',
        "JSON-LD": r'<script[^>]+type=["\']application/ld\+json["\']',
    }
    for label, pattern in required.items():
        if not re.search(pattern, source, flags=re.I | re.S):
            errors.append(f"{rel}: missing {label}")

    if parser.h1 != 1:
        errors.append(f"{rel}: expected one H1, found {parser.h1}")

    for number, image in enumerate(parser.images, 1):
        for attribute in ("alt", "width", "height", "decoding"):
            if not image.get(attribute):
                errors.append(f"{rel}: image {number} missing {attribute}: {image.get('src')}")
        src = image.get("src") or ""
        target = local_target(page, src)
        if target and not target.exists():
            errors.append(f"{rel}: missing image file {src}")
        if target and target.suffix.lower() not in {".webp", ".avif", ".svg"}:
            errors.append(f"{rel}: non-optimized referenced image {src}")

    for href in parser.links:
        target = local_target(page, href)
        if target and not target.exists():
            errors.append(f"{rel}: broken local link {href}")

    for block in re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', source, flags=re.I | re.S):
        try:
            json.loads(block)
        except json.JSONDecodeError as exc:
            errors.append(f"{rel}: invalid JSON-LD ({exc})")

for xml_name in ("sitemap.xml", "feed.xml"):
    try:
        ElementTree.parse(ROOT / xml_name)
    except Exception as exc:
        errors.append(f"{xml_name}: invalid XML ({exc})")

referenced = set()
for path in [*ROOT.rglob("*.html"), ROOT / "styles.css", ROOT / "feed.xml", ROOT / "sitemap.xml"]:
    if path.exists() and not any(part == ".git" for part in path.parts):
        for match in re.findall(r'(?:(?:src|href|content)=["\']|url\(["\']?)([^"\')]+\.(?:webp|avif|svg))', path.read_text(encoding="utf-8"), flags=re.I):
            target = local_target(path, match)
            if target and target.exists():
                referenced.add(target)

total_bytes = sum(path.stat().st_size for path in referenced)
audited_count = sum(1 for page in html_files if not page.name.startswith(EXEMPT_PREFIXES))
print(f"Audited {audited_count} HTML pages")
print(f"Referenced optimized images: {len(referenced)}, {total_bytes / 1024 / 1024:.2f} MB")
if errors:
    print("\n".join(f"ERROR: {error}" for error in errors))
    sys.exit(1)
print("PASS: metadata, structured data, image attributes, XML and local links")
