# Gonzo Exotics — przygotowanie sprzedaży i ogłoszeń

## Status: przygotowanie, bez aktywnej sprzedaży

Ten katalog jest dokumentacją wdrożenia dla przyszłych funkcji. Publiczna strona nie ma obecnie produktów, cen, koszyka, płatności, formularza zamówienia ani publicznego dostępu do płatnych plików.

## Dwa rozdzielone modele

1. **Ebooki / treści cyfrowe** — przyszły katalog może kierować do zewnętrznego checkoutu dopiero po włączeniu `salesEnabled`, uzupełnieniu danych sprzedawcy i weryfikacji obowiązków.
2. **Zwierzęta i karmówka** — wyłącznie ogłoszenia z przyciskiem kontaktowym. Bez koszyka, automatycznej umowy i automatycznej płatności.

## Jedno miejsce konfiguracji

Publiczny plik `assets/js/shop-config.js` zawiera wyłącznie placeholdery danych sprzedawcy i puste katalogi. Nie dodawaj do niego sekretów, tokenów, danych klientów, danych płatniczych ani plików premium. Przed aktywacją sprawdź, czy wszystkie placeholdery zostały zastąpione poprawnymi danymi.

## Dokumentacja sprzedaży

Szablon `SALES-RECORD-TEMPLATE.csv` jest pusty. Nie wpisuj do niego transakcji ani danych kupujących w publicznym repozytorium. Skopiuj go do **niepublicznego** arkusza lub systemu księgowego z ograniczonym dostępem.

Pozostałe listy kontrolne pokazują zakres weryfikacji, nie stanowią porady prawnej, podatkowej ani interpretacji klasyfikacji działalności. Przy uruchomieniu skonsultuj faktyczny model działania z księgowym i — tam gdzie potrzebne — prawnikiem.

## Kolejność uruchomienia

1. Uzupełnij dane podmiotu i potwierdź formę działalności.
2. Przejdź wszystkie checklisty w tym katalogu.
3. Wybierz dostawcę checkoutu, który obsłuży wymagane informacje, dowody zgód i bezpieczne płatności.
4. Skonfiguruj niepubliczną ewidencję sprzedaży.
5. Opublikuj regulamin oraz politykę prywatności po uzupełnieniu i weryfikacji.
6. Dopiero wtedy ustaw `salesEnabled: true` i dodaj pojedynczy, przetestowany produkt.

## Bramka techniczna

- Pusty `checkoutUrl` oznacza brak przycisku zakupowego.
- E-book nie może być przechowywany jako publiczny asset GitHub Pages.
- Ogłoszenie zwierzęcia ma tylko kontakt; finalną decyzję i dokumenty prowadzi się indywidualnie.
- GitHub Pages nie pozwala samodzielnie skonfigurować pełnego zestawu nagłówków HTTP. Jeżeli będą konieczne, użyj warstwy CDN/proxy lub hostingu z kontrolą nagłówków.
