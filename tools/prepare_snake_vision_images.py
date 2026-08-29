from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/images/blog/jak-widzi-waz"
OUT.mkdir(parents=True, exist_ok=True)

SOURCES = [
    (Path(r"C:/Users/gonzo/Desktop/kamery_4_590x427.jpg"), "termogram-dlonie-roznice-temperatury"),
    (Path(r"C:/Users/gonzo/Desktop/do-snakes-see-the-world-as-a-thermal-imag-display-v0-kbsor71jsfkg1.webp"), "pyton-termogram-czlowiek-kontrast-cieplny"),
]

for source, stem in SOURCES:
    with Image.open(source) as loaded:
        image = ImageOps.exif_transpose(loaded).convert("RGB")
        width, height = image.size
        image.save(OUT / f"{stem}.webp", "WEBP", quality=82, method=6)
        for target_width in (480, 960):
            if target_width >= width:
                continue
            target_height = round(height * target_width / width)
            resized = image.resize((target_width, target_height), Image.Resampling.LANCZOS)
            resized.save(OUT / f"{stem}-{target_width}w.webp", "WEBP", quality=80, method=6)

for path in sorted(OUT.glob("*.webp")):
    with Image.open(path) as image:
        print(f"{path.relative_to(ROOT)}\t{image.width}x{image.height}\t{path.stat().st_size} B")
