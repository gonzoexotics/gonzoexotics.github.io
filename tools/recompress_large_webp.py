from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
LIMIT = 700 * 1024


def main() -> None:
    for path in ROOT.rglob("*.webp"):
        if path.stat().st_size <= LIMIT:
            continue

        with Image.open(path) as image:
            temp = path.with_suffix(".optimized.webp")
            image.save(temp, "WEBP", quality=60, method=6)

        before = path.stat().st_size
        after = temp.stat().st_size
        if after < before:
            temp.replace(path)
            print(f"{path.relative_to(ROOT)}: {before / 1024:.0f} KB -> {after / 1024:.0f} KB")
        else:
            temp.unlink()


if __name__ == "__main__":
    main()
