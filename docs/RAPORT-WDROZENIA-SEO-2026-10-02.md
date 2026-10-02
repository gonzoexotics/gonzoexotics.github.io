# Raport wdrożenia SEO — Gonzo Exotics

Stan raportu: 02.10.2026. Ten dokument rozróżnia zmiany potwierdzone w repozytorium i na produkcji od danych, których nie można rzetelnie wywnioskować bez dostępu do GSC, danych terenowych albo dokumentacji pochodzenia zdjęć.

## 1. Co wdrożono

- Zachowano istniejące URL-e pillar pages: `corallus-caninus.html`, `morelia-viridis.html` i `python-bivittatus.html`; nie wykonano migracji `.html`.
- Baza Wiedzy otrzymała sześć widocznych hubów: trzy gatunkowe, start i terrarium, teju/obserwacje oraz osobny dział surykatki. Chronologiczna lista wpisów została zachowana.
- Dodano widoczne breadcrumbs do pillar pages, strony autora, praw do zdjęć i płatnego e-booka, wraz z `BreadcrumbList` tam, gdzie jest stosowany.
- Dodano stronę autora `o-autorze.html`, jednolitą encję `Person` oraz widoczne byline'y „Autor: Tomasz Gonsior • Gonzo Exotics” w 15 artykułach Bazy Wiedzy.
- Rozbudowano `porownaj-weze/` i `jaki-waz-dla-ciebie/` o statyczną treść, FAQ, linki do pillar pages i bezpieczne zastrzeżenia edukacyjne.
- Dodano stronę `prawa-do-zdjec.html`; cztery fotografie już opisane jako materiały Gonzo Exotics otrzymały w galerii `creator`, `copyrightNotice`, `license` i `acquireLicensePage`.
- Uzupełniono breadcrumbs i encję autora na stronie płatnego e-booka.
- Poprawiono opis miotu `Python bivittatus` 2026: 24.07.2026, 27 jaj, 25 żywo wyklutych młodych; samica jest opisana jako Albino Classic, bez niepotwierdzonego het Granite.
- Wdrożono plan 30 tematów i harmonogram 90 dni w `docs/SEO-ROADMAP-90-DNI.md`.

## 2. Technical SEO i testy

### Potwierdzone

- Wszystkie 29 URL-i z produkcyjnego `sitemap.xml` zwróciło HTTP 200 oraz miało title, self-canonical i dokładnie jeden H1.
- Lokalny crawl po drugim wdrożeniu: 33 pliki HTML, 31 poprawnie parsujących się bloków JSON-LD, brak uszkodzonych lokalnych odnośników i brak powielonych title, description lub canonical.
- W 347 tagach `img` nie stwierdzono brakującego `alt`. Pięć obrazów bez deklarowanych wymiarów to elementy lightboxa (`Powiększone zdjęcie`), nie zdjęcia w normalnym układzie treści.
- Kluczowe widoki desktopowe i mobilne zostały sprawdzone w przeglądarce. Dla Bazy Wiedzy, strony autora, praw do zdjęć, porównywarki i strony e-booka nie wykryto poziomego przewijania ani błędów konsoli.
- Logika narzędzi doboru węża przeszła testy danych, zdjęć, renderowania oraz 432 profili odpowiedzi.

### Celowo niezmienione

- `salesEnabled` pozostaje `false`.
- Nie zmieniono działających URL-i, nie utworzono masowych stron „A vs B”, nie usunięto wartościowych wpisów i nie ponowiono zgłoszenia poprawnej sitemap do GSC.

## 3. Architektura i linkowanie

Pillars są punktami nadrzędnymi, a huby Bazy Wiedzy prowadzą do powiązanych wpisów. Dodano relacje pillar ↔ supporting article, w tym Corallus caninus ↔ sezonowość/wilgotność, Morelia viridis ↔ lokalności/neonaty oraz Python bivittatus ↔ żywienie/genetyka/dokumentacja miotu. Porównanie Corallus caninus i Morelia viridis jest traktowane jako materiał wspierający, nie zastępnik obu pillar pages.

## 4. E-E-A-T, schema i obrazy

Encja autora jest teraz spójna w schema artykułów i na stronie autora. Treści nie dopisują niepotwierdzonych kwalifikacji ani doświadczeń. Dane licencyjne obrazów wdrożono tylko tam, gdzie istniejące opisy już wskazywały Gonzo Exotics jako źródło. Fotografie z innym kredytem lub bez jasnego potwierdzenia pochodzenia nie zostały automatycznie przypisane Tomaszowi Gonsiorowi ani objęte fałszywą licencją.

## 5. Wyniki wyszukiwania i GSC

Wykonano bieżący przegląd wyników dla fraz Corallus caninus, Morelia viridis i Python bivittatus. Wyniki są mieszane: specjalistyczne hodowle, fora, sklepowe poradniki i starsze opracowania. To wspiera strategię oparcia serwisu na autorstwie, własnej dokumentacji, artykułach źródłowych i klastrach, ale nie jest dowodem pozycji Gonzo Exotics.

Brak dostępu do konta Google Search Console w tym środowisku oznacza, że nie raportujemy kliknięć, wyświetleń, CTR, pozycji ani zapytań 4–20. Gdy GSC zbierze dane, należy je odczytać przed wyborem kolejnych tematów.

## 6. Performance i elementy do monitorowania

Nie stwierdzono regresji układu w sprawdzonych widokach, lecz nie ma podstaw do podawania wyniku LCP, INP, CLS ani TTFB bez Lighthouse/PageSpeed i danych CrUX. Te wartości wymagają osobnego pomiaru laboratoryjnego i danych terenowych po okresie zbierania.

Do kontroli po wdrożeniu:

1. GSC: indeksowanie sitemap, błędy, strony i zapytania z pozycją 4–20 oraz CTR.
2. GA4: przejścia hub → pillar → artykuł i pobrania materiałów.
3. Core Web Vitals: LCP, INP i CLS z danych terenowych.
4. Prawa do obrazów: przypisać źródło/zgodę do pozostałych plików przed rozszerzeniem ImageObject na całą bibliotekę.
5. Publikować backlog stopniowo; każdy nowy artykuł musi przejść niezależną weryfikację merytoryczną i linkowanie do właściwego pillara.

## Wniosek

Fundament techniczny, architektura informacji, E-E-A-T, indeksowalna część narzędzi i kluczowe korekty są wdrożone oraz przetestowane na produkcji. Części zależne od danych zewnętrznych, praw do konkretnych zdjęć i czasu — GSC, Core Web Vitals, pozycje oraz naturalne linki — nie są „zakończone” w dniu publikacji i muszą być monitorowane, a nie deklarowane bez dowodu.
