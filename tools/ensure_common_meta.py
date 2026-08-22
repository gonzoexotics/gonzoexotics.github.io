from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def insert_after(text: str, pattern: str, addition: str) -> str:
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    if not match:
        return text
    return text[: match.end()] + addition + text[match.end() :]


for path in sorted(ROOT.rglob("*.html")):
    if path.name.startswith("google") or "tools" in path.parts:
        continue
    text = path.read_text(encoding="utf-8")

    common = []
    if not re.search(r'<meta\s+name=["\']author["\']', text, re.I):
        common.append('\n<meta name="author" content="Gonzo Exotics">')
    if not re.search(r'<meta\s+name=["\']robots["\']', text, re.I):
        common.append('\n<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">')
    if not re.search(r'<meta\s+name=["\']theme-color["\']', text, re.I):
        common.append('\n<meta name="theme-color" content="#070907">')
    if common:
        text = insert_after(text, r'<meta\s+name=["\']description["\'][^>]*>', "".join(common))

    if not re.search(r'<link\s+rel=["\']alternate["\'][^>]*application/rss\+xml', text, re.I):
        depth = len(path.relative_to(ROOT).parents) - 1
        feed = "../" * depth + "feed.xml"
        addition = f'\n<link rel="alternate" type="application/rss+xml" title="Blog Gonzo Exotics" href="{feed}">'
        if re.search(r'<link\s+rel=["\']canonical["\']', text, re.I):
            text = insert_after(text, r'<link\s+rel=["\']canonical["\'][^>]*>', addition)
        else:
            text = text.replace("</head>", addition + "\n</head>", 1)

    if re.search(r'<meta\s+property=["\']og:type["\']', text, re.I):
        additions = []
        if not re.search(r'<meta\s+property=["\']og:locale["\']', text, re.I):
            additions.append('\n<meta property="og:locale" content="pl_PL">')
        if not re.search(r'<meta\s+property=["\']og:site_name["\']', text, re.I):
            additions.append('\n<meta property="og:site_name" content="Gonzo Exotics">')
        if additions:
            text = insert_after(text, r'<meta\s+property=["\']og:type["\'][^>]*>', "".join(additions))

    path.write_text(text, encoding="utf-8", newline="\n")

print("Common metadata normalized for all indexable HTML pages")
