/* Publiczna konfiguracja katalogów. Nie zapisuj tu haseł, kluczy API, danych klientów ani płatnych plików. */
window.GONZO_SHOP_CONFIG = Object.freeze({
  mode: "prelaunch",
  salesEnabled: false,
  seller: Object.freeze({
    legalName: "[NAZWA GONZO EXOTICS]",
    ownerName: "[IMIĘ I NAZWISKO]",
    correspondenceAddress: "[ADRES DO KORESPONDENCJI]",
    email: "[E-MAIL]",
    phone: "[TELEFON]",
    taxId: "[NIP – JEŻELI WYMAGANY]"
  }),
  digitalProducts: [],
  animalAds: [],
  adCategories: ["Corallus caninus","Morelia viridis","Python bivittatus","Pozostałe zwierzęta","Karmówka","Archiwum"]
});