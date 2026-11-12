(() => {
  const items = window.GONZO_SHOP_CONFIG?.animalAds;
  const container = document.getElementById('ads-catalog');
  if (!container || !Array.isArray(items)) return;
  const visible = items.filter(item => item && item.status === 'published');
  if (!visible.length) return;
  const status = document.getElementById('availability-status');
  const heading = document.getElementById('ads-title');
  if (status) status.textContent = 'Current listings appear below.';
  if (heading) heading.textContent = 'Current listings';
  const element = (tag, value, cls) => { const n = document.createElement(tag); n.textContent = String(value); if (cls) n.className = cls; return n; };
  const cards = visible.map(item => {
    const card = element('article', '', 'catalog-card');
    card.append(element('span', 'Available', 'catalog-status'));
    const title = element('h3', item.titleEn || item.title || item.species || 'Animal listing');
    if (item.title && !item.titleEn) { title.lang = 'pl'; card.append(element('p', 'Listing title in Polish', 'catalog-meta')); }
    card.append(title);
    const labels = { description: 'Description', hatchDate: 'Hatch or birth date', sex: 'Sex', feeding: 'Feeding', origin: 'Origin', documentStatus: 'Documentation' };
    for (const [key, label] of Object.entries(labels)) {
      const raw = item[key]; const translated = item[key + 'En'];
      if (!raw && !translated) continue;
      const line = element('p', '', 'catalog-meta');
      line.append(element('strong', label + ': '));
      const value = element('span', translated || raw);
      if (!translated && key !== 'hatchDate') { value.lang = 'pl'; line.append(element('span', 'Original Polish text: ')); }
      line.append(value); card.append(line);
    }
    if (item.contactUrl) { const a = element('a', 'Enquire about this animal', 'commerce-link'); a.href = item.contactUrl; card.append(a); }
    return card;
  });
  container.replaceChildren(...cards);
})();