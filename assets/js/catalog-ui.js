(() => {
  const config = window.GONZO_SHOP_CONFIG;
  if (!config) return;
  const sellerReady = Object.values(config.seller).every(value => typeof value === "string" && value.trim() && !value.includes("["));
  const text = (tag, value, className) => { const node=document.createElement(tag); node.textContent=value; if(className) node.className=className; return node; };
  function card(item, type) {
    const article=document.createElement("article"); article.className="catalog-card";
    article.append(text("span", item.status === "coming_soon" ? "W przygotowaniu" : "Dostępne", "catalog-status"));
    article.append(text("h3", item.title || item.species || "Bez tytułu"));
    article.append(text("p", item.description || "", "catalog-meta"));
    const meta=[];
    if(type==="ebooks"){ if(item.pages) meta.push(item.pages+" stron"); if(item.version) meta.push("wersja "+item.version); if(item.publicationDate) meta.push("publikacja: "+item.publicationDate); }
    else { ["hatchDate","sex","feeding","status"].forEach(key=>item[key]&&meta.push(item[key])); }
    if(meta.length) article.append(text("p",meta.join(" • "),"catalog-meta"));
    // Ebook może dostać zewnętrzny link dopiero po aktywacji sprzedaży i weryfikacji danych.
    if(type==="ebooks" && config.salesEnabled && sellerReady && item.checkoutUrl) {
      const link=document.createElement("a"); link.href=item.checkoutUrl; link.className="commerce-link"; link.textContent="Przejdź do bezpiecznej płatności"; article.append(link);
    }
    if(type==="ads" && item.contactUrl) { const link=document.createElement("a"); link.href=item.contactUrl; link.className="commerce-link"; link.textContent="Zapytaj o zwierzę"; article.append(link); }
    return article;
  }
  document.querySelectorAll("[data-catalog]").forEach(container => {
    const type=container.dataset.catalog;
    const source=type==="ebooks" ? config.digitalProducts : config.animalAds;
    const visible=source.filter(item => item && item.status==="published");
    if(!visible.length) return;
    container.replaceChildren(...visible.map(item=>card(item,type)));
  });
})();