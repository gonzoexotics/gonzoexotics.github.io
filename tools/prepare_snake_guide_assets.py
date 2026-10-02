"""Download eight named Wikimedia Commons photographs and create local WebP derivatives.

The title, creator and licence of each asset are recorded in
assets/images/snake-guide/CREDITS.md.  This script is intentionally explicit:
it must not be used to pull unreviewed search results into the site.
"""
from io import BytesIO
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "images" / "snake-guide"
ASSETS = {
    "lampropeltis-triangulum": "File:Eastern Milk Snake (Lampropeltis triangulum triangulum) (40682943834).jpg",
    "pantherophis-obsoletus": "File:Black Rat Snake (Pantherophis obsoletus).jpg",
    "elaphe-schrenckii": "File:Elaphe schrenckii from South Korea.jpg",
    "boaedon-fuliginosus": "File:African House Snake 005.jpg",
    "eunectes-notaeus": "File:Eunectes notaeus 54396531.jpg",
    "eunectes-murinus": "File:Anaconda común (Eunectes murinus), Tierpark Hellabrunn, Múnich, Alemania, 2012-06-17, DD 01.JPG",
    "malayopython-reticulatus": "File:Malayopython reticulatus, Reticulated python - Kaeng Krachan District, Phetchaburi Province (47924282891).jpg",
    "boiga-dendrophila": "File:Ularburong Boiga dendrophila.jpg",
}


def thumbnail_url(title: str) -> str:
    return "https://commons.wikimedia.org/wiki/Special:FilePath/" + quote(title.replace("File:", ""), safe="") + "?width=900"


OUT.mkdir(parents=True, exist_ok=True)
for stem, title in ASSETS.items():
    source = thumbnail_url(title)
    request = Request(source, headers={"User-Agent": "GonzoExotics-image-crediting/1.0 (contact@gonzoexotics.pl)"})
    with urlopen(request, timeout=60) as response:
        original = Image.open(BytesIO(response.read())).convert("RGB")
    original.thumbnail((900, 900), Image.Resampling.LANCZOS)
    target = OUT / f"{stem}.webp"
    original.save(target, "WEBP", quality=82, method=6)
    print(f"{target.name}: {original.width}×{original.height}")
