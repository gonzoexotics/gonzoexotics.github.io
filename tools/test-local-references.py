"""Check that local HTML links and assets resolve inside the published site."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKIP_PREFIXES = ('#', 'data:', 'mailto:', 'tel:', 'javascript:', 'http:', 'https:', '//')


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.values = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        for attribute in ('href', 'src', 'action'):
            if values.get(attribute):
                self.values.append(values[attribute])
        if values.get('srcset'):
            for candidate in values['srcset'].split(','):
                self.values.append(candidate.strip().split(' ', 1)[0])


def local_target(page: Path, value: str) -> Path | None:
    if not value or value.startswith(SKIP_PREFIXES):
        return None
    path = unquote(urlsplit(value).path)
    if not path:
        return None
    if path.startswith('/'):
        return ROOT / path.lstrip('/')
    return page.parent / path


errors = []
for page in ROOT.rglob('*.html'):
    if '.git' in page.parts:
        continue
    parser = References()
    parser.feed(page.read_text(encoding='utf-8'))
    for value in parser.values:
        target = local_target(page, value)
        if target is not None and not target.resolve().exists():
            errors.append(f'{page.relative_to(ROOT)} -> {value}')

if errors:
    raise SystemExit('Broken local references:\n' + '\n'.join(errors))
print('PASS: all local HTML links, forms and asset references resolve.')
