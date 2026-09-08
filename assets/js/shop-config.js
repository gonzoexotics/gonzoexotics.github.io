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
  // To są nazwy wymaganych pól przyszłych rekordów, a nie aktywne produkty ani ogłoszenia.
  schemas: Object.freeze({
    digitalProductFields: ["title", "slug", "cover", "description", "price", "currency", "pages", "version", "checkoutUrl", "status", "publicationDate"],
    animalAdFields: ["id", "species", "category", "hatchDate", "sex", "feeding", "origin", "documentStatus", "photos", "status", "contactUrl"]
  }),
  digitalProducts: [],
  animalAds: [],
  adCategories: ["Corallus caninus","Morelia viridis","Python bivittatus","Pozostałe zwierzęta","Karmówka","Archiwum"]
});