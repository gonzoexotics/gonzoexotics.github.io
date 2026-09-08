# Security checklist

- [ ] Zawsze używaj HTTPS; nie uruchamiaj sprzedaży bez poprawnego certyfikatu.
- [ ] Trzymaj dane klientów i ewidencję poza publicznym repozytorium.
- [ ] Nie umieszczaj sekretów ani tokenów w JavaScript, HTML lub historii Git.
- [ ] Używaj zewnętrznego operatora płatności; strona nie obsługuje numerów kart.
- [ ] Używaj `rel="noopener noreferrer"` dla linków zewnętrznych otwieranych w nowej karcie.
- [ ] Utrzymuj `referrer` policy w metadanych stron.
- [ ] Przed aktywacją sprawdź zależności, linki checkoutu i uprawnienia skrzynek.
- [ ] GitHub Pages nie pozwala samodzielnie ustawić pełnego CSP ani nagłówka `X-Content-Type-Options`; nie deklaruj ich jako wdrożonych. Jeśli są wymagane, skonfiguruj je przez CDN/proxy lub inny hosting.
- [ ] Przeglądaj okresowo historię repozytorium pod kątem przypadkowo dodanych danych.
