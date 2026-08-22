from __future__ import annotations

import posixpath
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SITE = "https://gonzoexotics.github.io/"
MAX_DIMENSION = 1920
WEBP_QUALITY = 82

IMAGE_URL_RE = re.compile(
    r"(?:https://gonzoexotics\.github\.io/|(?<![\w:/])/?(?:\.\./|\./)*)"
    r"[^\s\"'()<>]+?\.(?:jpe?g|png)(?:\?[^\s\"'()<>]*)?(?:#[^\s\"'()<>]*)?",
    re.IGNORECASE,
)
IMG_TAG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE | re.DOTALL)
ATTR_RE = lambda name: re.compile(
    rf"\s+{re.escape(name)}\s*=\s*(?:\"[^\"]*\"|'[^']*'|[^\s>]+)",
    re.IGNORECASE,
)


V15_NAMES = {
    1: "python-bivittatus-albino-portret",
    2: "python-bivittatus-albino-pobieranie-pokarmu",
    3: "morelia-viridis-zolty-mlody",
    4: "morelia-viridis-pobieranie-pokarmu",
    5: "morelia-viridis-zolty-na-zerdzi",
    6: "morelia-viridis-zielony-na-zerdzi",
    7: "waz-egzotyczny-jasny-w-dloni",
    8: "morelia-viridis-zielony-odpoczynek",
    9: "morelia-viridis-zielony-zblizenie-glowy",
    10: "python-bivittatus-jasny-zblizenie-glowy",
    11: "morelia-viridis-zielony-zwiniety",
    12: "python-bivittatus-samica-z-jajami",
    13: "python-bivittatus-jaja",
    14: "python-bivittatus-inkubacja-jaj",
    15: "morelia-viridis-zielony-w-terrarium",
    16: "morelia-viridis-zielony-odpoczynek-2",
    17: "python-bivittatus-albino-dorosly-1",
    18: "python-bivittatus-albino-dorosly-2",
    19: "morelia-viridis-czerwony-neonat",
    20: "python-bivittatus-albino-dorosly-3",
    21: "python-bivittatus-jasny-mlody-1",
    22: "python-bivittatus-jasny-mlody-2",
    23: "python-bivittatus-jasny-mlody-3",
    24: "python-bivittatus-klucie-z-jaja-1",
    25: "python-bivittatus-klucie-z-jaja-2",
    26: "python-bivittatus-inkubator-z-jajami",
    27: "morelia-viridis-zielony-zblizenie",
    28: "morelia-viridis-zielony-na-zerdzi-2",
    29: "python-bivittatus-inkubacja-jaj-2",
    30: "morelia-viridis-zielony-mlody",
    31: "python-bivittatus-klasyczny-mlody-1",
    32: "python-bivittatus-klasyczny-mlody-2",
    33: "python-bivittatus-jasny-mlody-4",
    34: "python-bivittatus-albino-mlody",
    35: "morelia-viridis-zielony-na-zerdzi-3",
    36: "python-bivittatus-mlode-w-pojemniku",
    37: "python-bivittatus-brazowy-mlody-1",
    38: "python-bivittatus-jasny-mlody-5",
    39: "python-bivittatus-jasny-mlody-6",
    40: "python-bivittatus-brazowy-mlody-2",
}


def relative_path(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def destination_for(source_rel: str) -> str:
    source_rel = source_rel.replace("\\", "/")
    match = re.fullmatch(r"assets/morelia/morelia-(\d+)\.jpe?g", source_rel, re.I)
    if match:
        n = int(match.group(1))
        return f"assets/images/gallery/morelia-viridis/morelia-viridis-galeria-{n:02}.webp"

    match = re.fullmatch(r"assets/corallus/corallus-(\d+)\.jpe?g", source_rel, re.I)
    if match:
        n = int(match.group(1))
        return f"assets/images/gallery/corallus-caninus/corallus-caninus-galeria-{n:02}.webp"

    match = re.fullmatch(r"assets/gallery-(\d+)\.jpe?g", source_rel, re.I)
    if match:
        n = int(match.group(1))
        species = "morelia-viridis" if n <= 19 or n >= 31 else "python-bivittatus"
        return f"assets/images/gallery/{species}/{species}-hodowla-{n:02}.webp"

    match = re.fullmatch(r"assets/galeria-v15/galeria-(\d+)\.jpe?g", source_rel, re.I)
    if match:
        n = int(match.group(1))
        name = V15_NAMES[n]
        if name.startswith("morelia-viridis"):
            folder = "morelia-viridis"
        elif name.startswith("python-bivittatus"):
            folder = "python-bivittatus"
        else:
            folder = "pozostale"
        return f"assets/images/gallery/{folder}/{name}-gonzo-exotics.webp"

    special = {
        "assets/biak.jpg": "assets/images/site/morelia-viridis-biak-tlo-gonzo-exotics.webp",
        "assets/morelia-card-v7.jpg": "assets/images/site/morelia-viridis-karta-gatunku-gonzo-exotics.webp",
        "assets/morelia-card.jpg": "assets/images/site/morelia-viridis-karta-gatunku-archiwum.webp",
        "assets/morelia-viridis.jpg": "assets/images/site/morelia-viridis-gonzo-exotics.webp",
        "assets/corallus-card.jpg": "assets/images/site/corallus-caninus-karta-gatunku-gonzo-exotics.webp",
        "assets/corallus-caninus.jpg": "assets/images/site/corallus-caninus-gonzo-exotics.webp",
        "assets/python-bivittatus.jpg": "assets/images/site/python-bivittatus-gonzo-exotics.webp",
    }
    if source_rel in special:
        return special[source_rel]

    source = Path(source_rel)
    return source.with_suffix(".webp").as_posix()


def resolve_local_url(raw_url: str, owner: Path) -> tuple[str, str] | None:
    parts = urlsplit(raw_url)
    clean = parts.path
    if raw_url.startswith(SITE):
        source = ROOT / clean.lstrip("/")
        kind = "absolute"
    elif clean.startswith("/"):
        source = ROOT / clean.lstrip("/")
        kind = "root"
    else:
        source = owner.parent / clean
        kind = "relative"
    try:
        source_rel = relative_path(source)
    except ValueError:
        return None
    if not (ROOT / source_rel).exists():
        return None
    return source_rel, kind


def format_new_url(target_rel: str, raw_url: str, owner: Path, kind: str) -> str:
    parts = urlsplit(raw_url)
    if kind == "absolute":
        path = "/" + target_rel
        return urlunsplit((parts.scheme, parts.netloc, path, parts.query, parts.fragment))
    if kind == "root":
        path = "/" + target_rel
    else:
        owner_rel = owner.parent.resolve().relative_to(ROOT).as_posix()
        path = posixpath.relpath(target_rel, owner_rel or ".")
    return urlunsplit(("", "", path, parts.query, parts.fragment))


def convert(source_rel: str, target_rel: str) -> tuple[int, int]:
    source = ROOT / source_rel
    target = ROOT / target_rel
    target.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as image:
        image = ImageOps.exif_transpose(image)
        if max(image.size) > MAX_DIMENSION:
            image.thumbnail((MAX_DIMENSION, MAX_DIMENSION), Image.Resampling.LANCZOS)
        if image.mode not in {"RGB", "RGBA"}:
            image = image.convert("RGB")
        image.save(target, "WEBP", quality=WEBP_QUALITY, method=6)
        return image.size


def local_image_path(src: str, owner: Path) -> Path | None:
    parts = urlsplit(src)
    path = parts.path
    if src.startswith(SITE):
        candidate = ROOT / path.lstrip("/")
    elif path.startswith("/"):
        candidate = ROOT / path.lstrip("/")
    else:
        candidate = owner.parent / path
    try:
        candidate.resolve().relative_to(ROOT)
    except ValueError:
        return None
    return candidate if candidate.exists() else None


def inferred_alt(src: str) -> str:
    stem = Path(urlsplit(src).path).stem
    if "morelia-viridis" in stem:
        return "Pyton zielony (Morelia viridis) w hodowli Gonzo Exotics"
    if "corallus-caninus" in stem:
        return "Corallus caninus zwinięty na żerdzi w hodowli Gonzo Exotics"
    if "python-bivittatus" in stem:
        return "Pyton birmański (Python bivittatus) w hodowli Gonzo Exotics"
    return "Wąż egzotyczny z hodowli Gonzo Exotics"


def optimize_img_tags(html: str, owner: Path) -> tuple[str, str | None]:
    image_index = 0
    first_src: str | None = None

    def replace_tag(match: re.Match[str]) -> str:
        nonlocal image_index, first_src
        tag = match.group(0)
        src_match = re.search(r"\bsrc\s*=\s*([\"'])(.*?)\1", tag, re.I | re.S)
        if not src_match:
            return tag
        src = src_match.group(2)
        image_path = local_image_path(src, owner)
        if image_path is None:
            return tag
        with Image.open(image_path) as image:
            width, height = image.size
        if first_src is None:
            first_src = src

        alt_match = re.search(r"\balt\s*=\s*([\"'])(.*?)\1", tag, re.I | re.S)
        if alt_match:
            alt = alt_match.group(2).strip()
            generic = (
                not alt
                or alt.startswith("Galeria Gonzo Exotics")
                or alt in {
                    "Morelia viridis — Gonzo Exotics",
                    "Corallus caninus — Gonzo Exotics",
                    "Python bivittatus — Gonzo Exotics",
                }
            )
            if generic:
                new_alt = inferred_alt(src)
                tag = tag[: alt_match.start(2)] + new_alt + tag[alt_match.end(2) :]

        for attribute in ("width", "height", "loading", "decoding", "fetchpriority"):
            tag = ATTR_RE(attribute).sub("", tag)

        priority = image_index == 0
        image_index += 1
        attrs = f' width="{width}" height="{height}" decoding="async"'
        if priority:
            attrs += ' loading="eager" fetchpriority="high"'
        else:
            attrs += ' loading="lazy"'
        if tag.endswith("/>"):
            return tag[:-2].rstrip() + attrs + " />"
        return tag[:-1].rstrip() + attrs + ">"

    return IMG_TAG_RE.sub(replace_tag, html), first_src


def ensure_preload(html: str, first_src: str | None, owner: Path) -> str:
    if owner.name == "index.html":
        first_src = "assets/images/site/morelia-viridis-biak-tlo-gonzo-exotics.webp"
    if not first_src:
        return html
    if re.search(r'<link\s+[^>]*rel=["\']preload["\'][^>]*as=["\']image["\']', html, re.I):
        return html
    preload = f'  <link rel="preload" as="image" href="{first_src}" type="image/webp" fetchpriority="high">\n'
    return html.replace("</head>", preload + "</head>", 1)


def main() -> None:
    owners = [
        path
        for path in ROOT.rglob("*")
        if path.suffix.lower() in {".html", ".css", ".xml"}
        and path.name not in {"google8d675c9d26ef178b.html"}
        and "tools" not in path.parts
    ]
    refs: dict[str, str] = {}
    owner_text: dict[Path, str] = {}
    for owner in owners:
        text = owner.read_text(encoding="utf-8")
        owner_text[owner] = text
        for match in IMAGE_URL_RE.finditer(text):
            raw = match.group(0)
            resolved = resolve_local_url(raw, owner)
            if resolved:
                source_rel, _ = resolved
                refs[source_rel] = destination_for(source_rel)

    dimensions: dict[str, tuple[int, int]] = {}
    before = 0
    after = 0
    for source_rel, target_rel in sorted(refs.items()):
        source = ROOT / source_rel
        before += source.stat().st_size
        dimensions[target_rel] = convert(source_rel, target_rel)
        after += (ROOT / target_rel).stat().st_size

    for owner, text in owner_text.items():
        def replace_url(match: re.Match[str]) -> str:
            raw = match.group(0)
            resolved = resolve_local_url(raw, owner)
            if not resolved:
                return raw
            source_rel, kind = resolved
            target_rel = refs.get(source_rel)
            return format_new_url(target_rel, raw, owner, kind) if target_rel else raw

        updated = IMAGE_URL_RE.sub(replace_url, text)
        if owner.suffix.lower() == ".html":
            updated, first_src = optimize_img_tags(updated, owner)
            updated = ensure_preload(updated, first_src, owner)
        owner.write_text(updated, encoding="utf-8", newline="\n")

    print(f"Converted {len(refs)} referenced images")
    print(f"Referenced image payload: {before / 1024 / 1024:.2f} MB -> {after / 1024 / 1024:.2f} MB")


if __name__ == "__main__":
    main()
