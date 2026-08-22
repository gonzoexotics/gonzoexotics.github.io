from __future__ import annotations

from html import unescape
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    page
    for page in ROOT.rglob("*.html")
    if ".git" not in page.parts and "tools" not in page.parts and not page.name.startswith("google")
]


def attr(tag: str, name: str) -> str:
    match = re.search(rf'\b{name}=["\']([^"\']+)', tag, flags=re.I)
    return unescape(match.group(1).strip()) if match else ""


def add_before_close(tag: str, attributes: str) -> str:
    if tag.rstrip().endswith("/>"):
        return re.sub(r"\s*/>\s*$", f" {attributes} />", tag)
    return re.sub(r">\s*$", f" {attributes}>", tag)


def local_path(page: Path, reference: str) -> Path | None:
    parsed = urlsplit(unquote(reference))
    if parsed.scheme or parsed.netloc:
        prefix = "https://gonzoexotics.github.io/"
        if not reference.startswith(prefix):
            return None
        return ROOT / reference[len(prefix):]
    return (page.parent / parsed.path).resolve()


def image_dimensions(path: Path) -> tuple[int, int]:
    with Image.open(path) as image:
        return image.size


def build_variants(source: Path) -> list[tuple[Path, int]]:
    with Image.open(source) as opened:
        image = ImageOps.exif_transpose(opened).convert("RGB")
        width, height = image.size
        variants: list[tuple[Path, int]] = []
        for target_width in (480, 960):
            if width <= target_width:
                continue
            target = source.with_name(f"{source.stem}-{target_width}w.webp")
            target_height = round(height * target_width / width)
            resized = image.resize((target_width, target_height), Image.Resampling.LANCZOS)
            resized.save(target, "WEBP", quality=78, method=6)
            variants.append((target, target_width))
        variants.append((source, width))
        return variants


for page in sorted(PAGES):
    source = page.read_text(encoding="utf-8")
    depth = len(page.relative_to(ROOT).parents) - 1
    favicon = "../" * depth + "favicon.svg"

    if not re.search(r'<link[^>]+rel=["\'](?:shortcut )?icon["\']', source, flags=re.I):
        canonical = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]*>', source, flags=re.I)
        if canonical:
            icon_tag = f'\n  <link rel="icon" href="{favicon}" type="image/svg+xml" sizes="any" />'
            source = source[: canonical.end()] + icon_tag + source[canonical.end() :]

    og_alt_match = re.search(
        r'<meta[^>]+property=["\']og:image:alt["\'][^>]+content=["\']([^"\']+)',
        source,
        flags=re.I,
    )
    twitter_image_match = re.search(r'<meta[^>]+name=["\']twitter:image["\'][^>]*>', source, flags=re.I)
    if og_alt_match and twitter_image_match and "twitter:image:alt" not in source:
        value = og_alt_match.group(1)
        tag = f'\n  <meta name="twitter:image:alt" content="{value}" />'
        source = source[: twitter_image_match.end()] + tag + source[twitter_image_match.end() :]

    og_image_match = re.search(
        r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\'][^>]*>',
        source,
        flags=re.I,
    )
    if og_image_match and "og:image:width" not in source:
        og_path = local_path(page, og_image_match.group(1))
        if og_path and og_path.exists():
            width, height = image_dimensions(og_path)
            dimensions = (
                f'\n  <meta property="og:image:width" content="{width}" />'
                f'\n  <meta property="og:image:height" content="{height}" />'
            )
            source = source[: og_image_match.end()] + dimensions + source[og_image_match.end() :]

    preload_match = re.search(
        r'<link\b(?=[^>]*\brel=["\']preload["\'])(?=[^>]*\bas=["\']image["\'])[^>]*>',
        source,
        flags=re.I,
    )
    if preload_match:
        preload_tag = preload_match.group(0)
        href = attr(preload_tag, "href")
        original = local_path(page, href)
        if original and original.exists() and original.suffix.lower() == ".webp":
            variants = build_variants(original)
            if len(variants) > 1:
                srcset = ", ".join(
                    f"{href.rsplit('/', 1)[0] + '/' if '/' in href else ''}{variant.name} {width}w"
                    for variant, width in variants
                )
                sizes = "(max-width: 900px) 100vw, 50vw"
                new_preload = preload_tag
                if "imagesrcset=" not in preload_tag:
                    new_preload = add_before_close(
                        preload_tag,
                        f'imagesrcset="{srcset}" imagesizes="{sizes}"',
                    )
                    source = source[: preload_match.start()] + new_preload + source[preload_match.end() :]

                image_match = re.search(
                    rf'<img\b(?=[^>]*\bsrc=["\']{re.escape(href)}["\'])[^>]*>',
                    source,
                    flags=re.I,
                )
                if image_match and "srcset=" not in image_match.group(0):
                    new_image = add_before_close(
                        image_match.group(0),
                        f'srcset="{srcset}" sizes="{sizes}"',
                    )
                    source = source[: image_match.start()] + new_image + source[image_match.end() :]

    page.write_text(source, encoding="utf-8", newline="\n")

print(f"Enhanced {len(PAGES)} pages with favicon, social metadata and responsive hero images")
