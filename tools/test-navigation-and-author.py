import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = ('Strona główna', 'Gatunki', 'Baza wiedzy', 'Porównaj węże', 'Darmowe materiały', 'E-booki', 'Dostępność', 'O autorze', 'Kontakt')
EXPECTED_TARGETS = ('index.html', 'index.html#gatunki', 'baza-wiedzy.html', 'porownaj-weze/', 'ebooki.html', 'ebooki.html', 'ogloszenia.html', 'o-autorze.html', 'index.html#kontakt')


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            href = dict(attrs).get('href')
            if href:
                self.hrefs.append(href)


menu_errors, link_errors, author_errors, schema_errors, regulation_errors, runtime_menu_errors = [], [], [], [], [], []
for path in ROOT.rglob('*.html'):
    if '.git' in path.parts:
        continue
    text = path.read_text(encoding='utf-8')
    if 'class="main-nav"' in text:
        start = text.index('<nav class="main-nav"')
        end = text.index('</nav>', start) + len('</nav>')
        fragment = text[start:end]
        if tuple(re.findall(r'>([^<>]+)</a>', fragment)) != EXPECTED:
            menu_errors.append(str(path.relative_to(ROOT)))
        parser = Links(); parser.feed(fragment)
        prefix = '../' if path.parent.name in {'baza-wiedzy', 'porownaj-weze', 'jaki-waz-dla-ciebie', 'platne-ebooki'} else ''
        if tuple(parser.hrefs) != tuple(prefix + target for target in EXPECTED_TARGETS):
            menu_errors.append(f'{path.relative_to(ROOT)}: wrong destinations')
        for href in parser.hrefs:
            target = (path.parent / href.split('#', 1)[0]).resolve()
            if href and not href.startswith(('http:', 'https:', 'mailto:', '#')) and not target.exists():
                link_errors.append(f'{path.relative_to(ROOT)} -> {href}')
    if path.parent.name == 'baza-wiedzy' and 'Autor:' in text and 'Tomasz Gonsior' in text:
        if 'href="../o-autorze.html">Tomasz Gonsior</a>' not in text:
            author_errors.append(str(path.relative_to(ROOT)))
        payloads = re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', text, flags=re.DOTALL)
        records = []
        try:
            for payload in payloads:
                data = json.loads(payload)
                records.extend(data.get('@graph', [data]))
        except json.JSONDecodeError:
            schema_errors.append(f'{path.relative_to(ROOT)}: invalid JSON-LD')
            continue
        articles = [record for record in records if record.get('@type') in {'Article', 'BlogPosting'}]
        if len(articles) != 1:
            schema_errors.append(f'{path.relative_to(ROOT)}: expected one Article or BlogPosting')
        else:
            author = articles[0].get('author', {})
            if author.get('@type') != 'Person' or author.get('name') != 'Tomasz Gonsior' or author.get('url') != 'https://gonzoexotics.pl/o-autorze.html':
                schema_errors.append(f'{path.relative_to(ROOT)}: inconsistent author schema')

regulation = (ROOT / 'regulamin.html').read_text(encoding='utf-8').lower()
for forbidden in ('[nazwa gonzo exotics]', '[imię i nazwisko]', '[adres do korespondencji]', '[e-mail]', '[telefon]', '[nip – jeżeli wymagany]', 'wersja przygotowawcza'):
    if forbidden in regulation:
        regulation_errors.append(forbidden)
if '<meta name="robots" content="noindex,follow">' not in regulation:
    regulation_errors.append('regulamin must remain noindex until sales are launched')

script = (ROOT / 'script.js').read_text(encoding='utf-8')
if 'Płatne e-booki' in script:
    runtime_menu_errors.append('script.js must not inject an extra paid e-book menu item')

if menu_errors or link_errors or author_errors or schema_errors or regulation_errors or runtime_menu_errors:
    raise SystemExit('\n'.join(['menu=' + ', '.join(menu_errors), 'links=' + ', '.join(link_errors), 'author=' + ', '.join(author_errors), 'schema=' + ', '.join(schema_errors), 'regulamin=' + ', '.join(regulation_errors), 'runtime_menu=' + ', '.join(runtime_menu_errors)]))
print('PASS: 32 identical navigation menus, valid local menu targets, linked article authors, consistent author schema and a placeholder-free noindex regulation page.')
