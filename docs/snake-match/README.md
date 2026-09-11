# Gonzo Snake Match — utrzymanie i rozszerzanie

Strony: `/jaki-waz-dla-ciebie/` i `/porownaj-weze/`.

## Jedno źródło danych
`assets/js/snake-data.js` jest jedynym katalogiem gatunków dla obu narzędzi. Nowy gatunek dodaj wyłącznie tam, z pełnymi polami: nazwa naukowa, rozmiar dorosły, rekomendowane terrarium, mikroklimat, wentylacja, karmienie, koszty, ryzyka, ograniczenia twarde i źródła z datą kontroli.

Nie dopisuj gatunku, gdy brakuje źródeł lub nie ma pewności co do parametrów. Ustaw wtedy `needsReview: true`; silnik nie pokaże takiego profilu.

## Bezpieczeństwo
Wagi i blokady są w `assets/js/snake-engine.js`. Blokada ma pierwszeństwo przed punktacją. Dotyczy przede wszystkim za małej przestrzeni, gatunków wymagających zaawansowanego doświadczenia oraz nieakceptowanej dużej karmówki.

## Zdjęcia
Użyte zostały wyłącznie prywatne zdjęcia Gonzo Exotics dla Morelia viridis, Corallus caninus i Python bivittatus. Pozostałe profile mają uczciwy placeholder „Zdjęcie w przygotowaniu”. Po dodaniu prywatnego zdjęcia wpisz względną ścieżkę do pola `image`; nie używaj zdjęcia innego gatunku jako dekoracji.

## Test
Uruchom lokalnie: `node tools/test-snake-engine.js`. Test obejmuje kompletność danych, 30 profili i blokady krytyczne.
