from __future__ import annotations

from html import unescape
from pathlib import Path
from urllib.parse import unquote, urlsplit
import posixpath
import re

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SITE = "https://gonzoexotics.github.io/"
IMG_RE = re.compile(r"<img\b[^>]*\bsrc=[\"'][^\"']+[\"'][^>]*>", re.I | re.S)


def attr(tag: str, name: str) -> str:
    match = re.search(rf"\b{re.escape(name)}\s*=\s*([\"'])(.*?)\1", tag, re.I | re.S)
    return unescape(match.group(2).strip()) if match else ""


def set_attr(tag: str, name: str, value: str) -> str:
    pattern = re.compile(rf"\s+{re.escape(name)}\s*=\s*([\"']).*?\1", re.I | re.S)
    if pattern.search(tag):
        return pattern.sub(f' {name}="{value}"', tag, count=1)
    if tag.rstrip().endswith("/>"):
        return re.sub(r"\s*/>\s*$", f' {name}="{value}" />', tag)
    return re.sub(r">\s*$", f' {name}="{value}">', tag)


def local_path(page: Path, reference: str) -> Path | None:
    parsed = urlsplit(unquote(reference))
    if parsed.scheme or parsed.netloc:
        if not reference.startswith(SITE):
            return None
        candidate = ROOT / reference[len(SITE):].split("?", 1)[0].split("#", 1)[0]
    elif parsed.path.startswith("/"):
        candidate = ROOT / parsed.path.lstrip("/")
    else:
        candidate = page.parent / parsed.path
    try:
        candidate = candidate.resolve()
        candidate.relative_to(ROOT)
    except ValueError:
        return None
    return candidate if candidate.exists() else None


def url_for(page: Path, image: Path, original: str) -> str:
    if original.startswith(SITE):
        return SITE + image.relative_to(ROOT).as_posix()
    if original.startswith("/"):
        return "/" + image.relative_to(ROOT).as_posix()
    page_dir = page.parent.relative_to(ROOT).as_posix() or "."
    return posixpath.relpath(image.relative_to(ROOT).as_posix(), page_dir)


def variants(source: Path) -> list[tuple[Path, int]]:
    with Image.open(source) as opened:
        image = ImageOps.exif_transpose(opened)
        width, height = image.size
        if image.mode not in {"RGB", "RGBA"}:
            image = image.convert("RGB")
        choices: list[tuple[Path, int]] = []
        for target_width in (480, 960):
            if width <= target_width:
                continue
            target = source.with_name(f"{source.stem}-{target_width}w.webp")
            if not target.exists():
                target_height = round(height * target_width / width)
                resized = image.resize((target_width, target_height), Image.Resampling.LANCZOS)
                resized.save(target, "WEBP", quality=78, method=6)
            choices.append((target, target_width))
        choices.append((source, width))
        return choices


def sizes_for(page: Path, source: str, start: int, tag: str) -> str:
    if page.name == "galeria.html":
        return "(max-width: 900px) 50vw, 25vw"
    if 'fetchpriority="high"' in tag or "fetchpriority='high'" in tag:
        return "(max-width: 900px) 100vw, 50vw"
    before = source[:start]
    last_section = before.rfind("</section>")
    if before.rfind('class="full-gallery', last_section) >= 0:
        return "(max-width: 900px) 50vw, 25vw"
    if before.rfind('class="article-photo-pair', last_section) >= 0:
        return "(max-width: 650px) 100vw, 50vw"
    if before.rfind('class="cards', last_section) >= 0 or before.rfind('class="knowledge-grid', last_section) >= 0:
        return "(max-width: 760px) 100vw, 33vw"
    if page.name == "baza-wiedzy.html":
        return "(max-width: 760px) 100vw, 33vw"
    return "(max-width: 900px) 100vw, 960px"


def responsive_images(page: Path, html: str) -> tuple[str, int]:
    additions = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal additions
        tag = match.group(0)
        src = attr(tag, "src")
        path = local_path(page, src)
        if not path or path.suffix.lower() != ".webp" or re.search(r"-\d+w$", path.stem):
            return tag
        choices = variants(path)
        if len(choices) == 1:
            return tag
        srcset = ", ".join(f"{url_for(page, variant, src)} {width}w" for variant, width in choices)
        tag = set_attr(tag, "srcset", srcset)
        tag = set_attr(tag, "sizes", sizes_for(page, html, match.start(), tag))
        additions += 1
        return tag

    return IMG_RE.sub(replace, html), additions


def common_metadata(page: Path, html: str) -> str:
    depth = len(page.relative_to(ROOT).parents) - 1
    prefix = "../" * depth
    if 'name="color-scheme"' not in html:
        theme = re.search(r'<meta[^>]+name=["\']theme-color["\'][^>]*>', html, re.I)
        if theme:
            html = html[:theme.end()] + '\n  <meta name="color-scheme" content="dark" />' + html[theme.end():]
    if 'rel="manifest"' not in html:
        icon = re.search(r'<link[^>]+rel=["\'](?:shortcut )?icon["\'][^>]*>', html, re.I)
        if icon:
            html = html[:icon.end()] + f'\n  <link rel="manifest" href="{prefix}site.webmanifest" />' + html[icon.end():]
    html = re.sub(
        r'("(?:author|publisher)"\s*:\s*\{\s*"@type"\s*:\s*"Organization",)(?!\s*"@id")',
        r'\1 "@id": "https://gonzoexotics.github.io/#organization",',
        html,
    )
    return html


def main() -> None:
    pages = [p for p in ROOT.rglob("*.html") if ".git" not in p.parts and "tools" not in p.parts and not p.name.startswith("google")]
    changed_tags = 0
    for page in sorted(pages):
        source = page.read_text(encoding="utf-8")
        updated = common_metadata(page, source)
        updated, count = responsive_images(page, updated)
        changed_tags += count
        page.write_text(updated, encoding="utf-8", newline="\n")
    variants_count = sum(1 for p in ROOT.rglob("*-480w.webp")) + sum(1 for p in ROOT.rglob("*-960w.webp"))
    variants_bytes = sum(p.stat().st_size for p in ROOT.rglob("*-480w.webp")) + sum(p.stat().st_size for p in ROOT.rglob("*-960w.webp"))
    print(f"Enhanced {len(pages)} pages; responsive image tags updated: {changed_tags}")
    print(f"Responsive variants: {variants_count}, {variants_bytes / 1024 / 1024:.2f} MB")


if __name__ == "__main__":
    main()
