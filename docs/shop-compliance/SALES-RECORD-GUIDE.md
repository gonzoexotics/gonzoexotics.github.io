# Niepubliczna ewidencja sprzedaży i kontrola limitu

## Zasada bezpieczeństwa

Plik `SALES-RECORD-TEMPLATE.csv` jest wyłącznie pustym wzorem kolumn. Skopiuj go do prywatnego arkusza (np. dysku z kontrolą dostępu) albo programu księgowego. **Nie zapisuj w publicznym repozytorium** danych klientów, adresów, numerów dokumentów tożsamości, dowodów płatności ani wypełnionej ewidencji.

## Konfiguracja na dany rok

1. Otwórz `SALES-LIMIT-CONFIG.example.json`.
2. Zweryfikuj w źródle urzędowym aktualny limit oraz warunki, które rzeczywiście dotyczą Twojej działalności.
3. W prywatnym arkuszu wpisz do komórki `B1` zweryfikowany limit. Dla 2026 r. przykładowa wartość z konfiguracji to **10 813,50 PLN na kwartał** dla działalności nierejestrowanej — nie jest to automatyczna kwalifikacja Twojej działalności.
4. Zmień rok w formułach i zapisz datę weryfikacji źródła.

## Przykładowy układ prywatnego arkusza

Arkusz `Sprzedaz` otrzymuje nagłówki z CSV. W kolumnie:
- A — data,
- F — kwota brutto,
- H — status (np. `opłacone`).

W osobnym arkuszu `Kontrola limitu` można ustawić:

- `B1`: ręcznie wpisany, zweryfikowany limit kwartalny.
- `B2` (przychód Q1 2026): `=SUMIFS(Sprzedaz!F:F,Sprzedaz!H:H,"opłacone",Sprzedaz!A:A,">="&DATE(2026,1,1),Sprzedaz!A:A,"<"&DATE(2026,4,1))`
- `B3` (wykorzystanie limitu): `=IFERROR(B2/B1,0)`

Dodaj formatowanie warunkowe dla `B3`:
- od 80% — ostrzeżenie,
- od 90% — pilne ostrzeżenie,
- od 100% — blokada dalszej sprzedaży do czasu wyjaśnienia z księgowym.

Dla kolejnych kwartałów zmieniaj datę początku i końca w `SUMIFS`. Przedstawione formuły są wzorem technicznym; ich zastosowanie oraz sposób liczenia przychodu muszą zostać potwierdzone dla faktycznego modelu działalności.
