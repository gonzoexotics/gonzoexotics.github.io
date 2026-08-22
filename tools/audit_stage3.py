from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import re
import sys

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []


class Parser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.images: list[dict[str, str | None]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "img":
            values = dict(attrs)
            if values.get("src"):
                self.images.append(values)


def local(page: Path, value: str) -> Path | None:
    parsed = urlsplit(unquote(value))
    if parsed.scheme or parsed.netloc:
        if parsed.netloc != "gonzoexotics.github.io":
            return None
        candidate = ROOT / parsed.path.lstrip("/")
    elif parsed.path.startswith("/"):
        candidate = ROOT / parsed.path.lstrip("/")
    else:
        candidate = page.parent / parsed.path
    return candidate.resolve()


pages = [p for p in ROOT.rglob("*.html") if ".git" not in p.parts and "tools" not in p.parts and not p.name.startswith("google")]
image_total = 0
responsive_total = 0

for page in sorted(pages):
    source = page.read_text(encoding="utf-8")
    rel = page.relative_to(ROOT).as_posix()
    if 'rel="manifest"' not in source:
        errors.append(f"{rel}: missing manifest")
    if 'name="color-scheme"' not in source:
        errors.append(f"{rel}: missing color-scheme")
    parser = Parser()
    parser.feed(source)
    for image in parser.images:
        image_total += 1
        target = local(page, image.get("src") or "")
        if not target or not target.exists() or target.suffix.lower() != ".webp":
            continue
        with Image.open(target) as opened:
            width = opened.width
        if width > 480:
            if not image.get("srcset") or not image.get("sizes"):
                errors.append(f"{rel}: large image lacks responsive attributes: {image.get('src')}")
            else:
                responsive_total += 1

for page in (ROOT / "baza-wiedzy").glob("*.html"):
    source = page.read_text(encoding="utf-8")
    for block in re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', source, re.I | re.S):
        try:
            data = json.loads(block)
        except json.JSONDecodeError:
            continue
        serialized = json.dumps(data, ensure_ascii=False)
        if '"BlogPosting"' in serialized and 'https://gonzoexotics.github.io/#organization' not in serialized:
            errors.append(f"{page.relative_to(ROOT).as_posix()}: BlogPosting author lacks organization @id")

if not (ROOT / "404.html").exists():
    errors.append("missing 404.html")
try:
    json.loads((ROOT / "site.webmanifest").read_text(encoding="utf-8"))
except Exception as exc:
    errors.append(f"invalid site.webmanifest: {exc}")

print(f"Stage 3 audit: {len(pages)} pages, {image_total} images, {responsive_total} large responsive images")
if errors:
    print("\n".join(f"ERROR: {item}" for item in errors))
    sys.exit(1)
print("PASS: responsive images, manifest, dark color scheme, author identity and 404")
