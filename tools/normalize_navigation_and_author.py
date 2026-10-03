import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTHOR = 'Autor: Tomasz Gonsior • Gonzo Exotics'
AUTHOR_LINK = 'Autor: <a href="../o-autorze.html">Tomasz Gonsior</a> • Gonzo Exotics'


def menu(prefix: str) -> str:
    return (
        '<nav class="main-nav" aria-label="Główna nawigacja">'
        f'<a href="{prefix}index.html">Strona główna</a>'
        f'<a href="{prefix}index.html#gatunki">Gatunki</a>'
        f'<a href="{prefix}baza-wiedzy.html">Baza wiedzy</a>'
        f'<a href="{prefix}porownaj-weze/">Porównaj węże</a>'
        f'<a href="{prefix}ebooki.html">Darmowe materiały</a>'
        f'<a href="{prefix}ebooki.html">E-booki</a>'
        f'<a href="{prefix}ogloszenia.html">Dostępność</a>'
        f'<a href="{prefix}o-autorze.html">O autorze</a>'
        f'<a href="{prefix}index.html#kontakt">Kontakt</a>'
        '</nav>'
    )


changed = []
for path in ROOT.rglob('*.html'):
    if '.git' in path.parts:
        continue
    relative = path.relative_to(ROOT).as_posix()
    text = path.read_bytes().decode('utf-8')
    original = text
    if path.parent.name == 'baza-wiedzy' or path.parent.name in {'porownaj-weze', 'jaki-waz-dla-ciebie', 'platne-ebooki'}:
        prefix = '../'
    else:
        prefix = ''
    text = re.sub(
        r'<nav class="main-nav" aria-label="Główna nawigacja">.*?</nav>\r?\n?',
        lambda _: menu(prefix) + '\n',
        text,
        flags=re.DOTALL,
    )
    if path.parent.name == 'baza-wiedzy':
        text = text.replace(AUTHOR, AUTHOR_LINK)
    if text != original:
        path.write_bytes(text.encode('utf-8'))
        changed.append(relative)

print(f'Updated {len(changed)} files')
for item in changed:
    print(item)
