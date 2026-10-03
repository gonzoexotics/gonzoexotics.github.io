/* Publiczna konfiguracja katalogów. Nie zapisuj tu haseł, kluczy API, danych klientów ani płatnych plików. */
window.GONZO_SHOP_CONFIG = Object.freeze({
  mode: "external_checkout",
  salesEnabled: true,
  seller: Object.freeze({
    legalName: "Tomasz Gonsior",
    ownerName: "Tomasz Gonsior",
    brandName: "Gonzo Exotics",
    activityType: "działalność nierejestrowana",
    correspondenceAddress: "Osiedle Andaluzja 9/2/7, 41-949 Piekary Śląskie, Polska",
    email: "gonsiortomasz@gmail.com"
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
