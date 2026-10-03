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


menu_errors, link_errors, author_errors, schema_errors, regulation_errors, privacy_errors, phone_errors, runtime_menu_errors = [], [], [], [], [], [], [], []
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
for forbidden in ('[nazwa gonzo exotics]', '[imię i nazwisko]', '[adres do korespondencji]', '[e-mail]', '[telefon]', '[nip – jeżeli wymagany]', 'wersja przygotowawcza', 'dokument roboczy'):
    if forbidden in regulation:
        regulation_errors.append(forbidden)
if '<meta name="robots" content="noindex,follow">' not in regulation:
    regulation_errors.append('regulamin must remain noindex,follow')
for required in ('tomasz gonsior', 'osiedle andaluzja 9/2/7', '41-949 piekary śląskie', 'gonsiortomasz@gmail.com', '+48 724 523 225', '1koszyk', 'autopay', 'treści cyfrow', 'odstąpienia', 'reklamacj', 'prawa autorskie', 'polityka prywatności', 'wzór formularza odstąpienia od umowy'):
    if required not in regulation:
        regulation_errors.append('missing ' + required)

privacy = (ROOT / 'polityka-prywatnosci.html').read_text(encoding='utf-8').lower()
for required in ('sprzedaż e-booka przez 1koszyk', 'fsi sp. z o.o.', 'autopay', 'art. 6 ust. 1 lit. b rodo', 'art. 6 ust. 1 lit. c rodo', 'art. 6 ust. 1 lit. f rodo', 'prezesa urzędu ochrony danych osobowych'):
    if required not in privacy:
        privacy_errors.append('missing ' + required)

phone_pattern = re.compile(r'(?:\+48\s*724\s*523\s*225|\+48724523225|724\s*523\s*225)')
for path in ROOT.rglob('*.html'):
    if phone_pattern.search(path.read_text(encoding='utf-8')) and path.name != 'regulamin.html':
        phone_errors.append(str(path.relative_to(ROOT)))
if phone_pattern.search((ROOT / 'sitemap.xml').read_text(encoding='utf-8')):
    phone_errors.append('sitemap.xml')
if 'regulamin.html' in (ROOT / 'sitemap.xml').read_text(encoding='utf-8'):
    regulation_errors.append('regulamin must not be in sitemap.xml')

script = (ROOT / 'script.js').read_text(encoding='utf-8')
if 'Płatne e-booki' in script:
    runtime_menu_errors.append('script.js must not inject an extra paid e-book menu item')

if menu_errors or link_errors or author_errors or schema_errors or regulation_errors or privacy_errors or phone_errors or runtime_menu_errors:
    raise SystemExit('\n'.join(['menu=' + ', '.join(menu_errors), 'links=' + ', '.join(link_errors), 'author=' + ', '.join(author_errors), 'schema=' + ', '.join(schema_errors), 'regulamin=' + ', '.join(regulation_errors), 'privacy=' + ', '.join(privacy_errors), 'phone=' + ', '.join(phone_errors), 'runtime_menu=' + ', '.join(runtime_menu_errors)]))
print('PASS: navigation, local references, author schema, sales documents, noindex regulation and phone privacy checks pass.')
