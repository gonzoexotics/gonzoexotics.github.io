from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import re


ROOT = Path(__file__).resolve().parents[1]


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.images: list[dict[str, str | None]] = []
        self.links: list[dict[str, str | None]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "img":
            self.images.append(values)
        elif tag == "link":
            self.links.append(values)


for page in sorted(ROOT.rglob("*.html")):
    if ".git" in page.parts or "tools" in page.parts or page.name.startswith("google"):
        continue
    source = page.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(source)
    rel = page.relative_to(ROOT).as_posix()
    preload = next(
        (
            link.get("href")
            for link in parser.links
            if link.get("rel") == "preload" and link.get("as") == "image"
        ),
        None,
    )
    preload_size = None
    if preload:
        candidate = (page.parent / unquote(urlsplit(preload).path)).resolve()
        if candidate.exists():
            preload_size = round(candidate.stat().st_size / 1024)
    flags = {
        "favicon": bool(re.search(r'<link[^>]+rel=["\'](?:shortcut )?icon["\']', source, re.I)),
        "og_dimensions": "og:image:width" in source and "og:image:height" in source,
        "primary_image": "primaryImageOfPage" in source,
        "breadcrumb": "BreadcrumbList" in source,
        "responsive_images": any(image.get("srcset") for image in parser.images),
        "preload_kb": preload_size,
    }
    print(f"{rel}: {json.dumps(flags, ensure_ascii=False)}")
