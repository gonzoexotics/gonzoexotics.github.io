(function () {
  const app = document.getElementById('compare-app');
  if (!app || !window.GonzoSnakeData) return;

  const { species } = window.GonzoSnakeData;
  const params = new URLSearchParams(location.search);
  let chosen = (params.get('species') || '').split(',').filter(id => species.some(item => item.id === id)).slice(0, 3);
  const escapeHtml = value => String(value).replace(/[&<>"']/g, character => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[character]));
  const imageUrl = item => item.image.startsWith('http') ? item.image : `../${item.image}`;
  const image = (item, className, alt = '') => `<span class="${className}"><img src="${escapeHtml(imageUrl(item))}" alt="${escapeHtml(alt)}" decoding="async" referrerpolicy="no-referrer" width="164" height="140"></span>`;
  const credit = item => item.imageCredit ? `<p class="photo-credit">${item.imageCreditUrl ? `<a href="${escapeHtml(item.imageCreditUrl)}" target="_blank" rel="noopener noreferrer">${escapeHtml(item.imageCredit)}</a>` : escapeHtml(item.imageCredit)}</p>` : '';
  const section = (title, content) => `<details open><summary>${title}</summary><div>${content}</div></details>`;

  function card(item) {
    return `<article class="compare-card"><div class="snake-photo"><img src="${escapeHtml(imageUrl(item))}" alt="${escapeHtml(`${item.commonName} (${item.scientificName})`)}" loading="lazy" decoding="async" referrerpolicy="no-referrer"><span>Zdjęcie gatunku</span></div><div class="compare-card-copy"><h2><em>${escapeHtml(item.scientificName)}</em><br>${escapeHtml(item.commonName)}</h2>${credit(item)}<p>${escapeHtml(item.shortDescription)}</p>${section('Warunki i skala', `<p><strong>Długość dorosłego:</strong> ${item.adultLengthMin}–${item.adultLengthMax} cm</p><p><strong>Rekomendowane terrarium:</strong> ${escapeHtml(item.recommendedEnclosure)}</p><p><strong>Typ:</strong> ${escapeHtml(item.enclosureType)}</p>`)}${section('Mikroklimat', `<p><strong>Temperatura:</strong> ${escapeHtml(item.temperatureModel)}</p><p><strong>Wilgotność:</strong> ${escapeHtml(item.humidityModel)}</p><p><strong>Wentylacja:</strong> ${escapeHtml(item.ventilationImportance)}</p>`)}${section('Codzienność', `<p><strong>Aktywność:</strong> ${escapeHtml(item.activityLevel)} (${escapeHtml(item.activityPeriod)})</p><p><strong>Obsługa:</strong> ${escapeHtml(item.handlingPotential)}</p><p><strong>Karmienie:</strong> ${escapeHtml(item.typicalPrey)}</p><p><strong>Koszt startu:</strong> ${escapeHtml(item.startupCost)}</p>`)}${section('Plusy i wyzwania', `<p><strong>Plusy:</strong> ${escapeHtml(item.advantages.join('; '))}</p><p><strong>Wyzwania:</strong> ${escapeHtml(item.challenges.join('; '))}</p>`)}<p class="legal-note"><strong>Prawo:</strong> ${escapeHtml(item.legalNotes)}</p></div></article>`;
  }

  function picker() {
    const choices = species.map(item => `<button type="button" class="species-choice${chosen.includes(item.id) ? ' selected' : ''}" data-id="${escapeHtml(item.id)}" aria-pressed="${chosen.includes(item.id)}">${image(item, 'species-choice-photo')}<span class="species-choice-copy"><em>${escapeHtml(item.scientificName)}</em><span>${escapeHtml(item.commonName)}</span></span></button>`).join('');
    app.innerHTML = `<section class="compare-picker"><h2>Wybierz 2 lub 3 gatunki</h2><p>Każdy gatunek ma własne zdjęcie. Wybierz karty, które chcesz zestawić.</p><div class="species-picker" aria-label="Lista gatunków">${choices}</div><div class="quiz-actions"><button class="snake-button" type="button" data-action="compare" ${chosen.length < 2 ? 'disabled' : ''}>Porównaj wybrane (${chosen.length}/3)</button><button class="snake-button secondary" type="button" data-action="clear" ${chosen.length ? '' : 'disabled'}>Wyczyść</button></div></section>`;
  }

  function comparison() {
    const selected = chosen.map(id => species.find(item => item.id === id));
    app.innerHTML = `<section class="comparison-intro"><p class="snake-eyebrow">PORÓWNANIE GATUNKÓW</p><h2>Różnice, które naprawdę zmieniają hodowlę</h2><p>Parametry są praktycznym punktem wyjścia. Nie przenoś automatycznie ustawień między gatunkami — szczególnie między <em>Corallus caninus</em> a <em>Morelia viridis</em>.</p><button class="text-link" type="button" data-action="edit">Zmień wybór</button></section><div class="comparison-grid">${selected.map(card).join('')}</div><aside class="why-not"><h2>Jak czytać to porównanie?</h2><p>Największe różnice zwykle dotyczą finalnej skali terrarium, marginesu błędów mikroklimatu, karmówki i tego, czy gatunek jest realnie do obserwacji czy do okazjonalnej obsługi.</p></aside><div class="result-actions"><button class="snake-button secondary" type="button" data-action="share">Udostępnij porównanie</button><a class="snake-button secondary" href="../jaki-waz-dla-ciebie/">Przejdź do quizu</a></div>`;
  }

  async function share() {
    try {
      const url = location.href;
      if (navigator.share) await navigator.share({ title: 'Porównywarka węży — Gonzo Exotics', url });
      else if (navigator.clipboard) { await navigator.clipboard.writeText(url); alert('Link do porównania skopiowany.'); }
    } catch (_) {}
  }

  app.addEventListener('click', event => {
    const button = event.target.closest('button');
    if (!button) return;
    const id = button.dataset.id;
    if (id) {
      chosen = chosen.includes(id) ? chosen.filter(item => item !== id) : (chosen.length < 3 ? [...chosen, id] : chosen);
      picker();
      return;
    }
    if (button.dataset.action === 'compare') { history.replaceState(null, '', `?species=${encodeURIComponent(chosen.join(','))}`); comparison(); }
    if (button.dataset.action === 'clear') { chosen = []; history.replaceState(null, '', location.pathname); picker(); }
    if (button.dataset.action === 'edit') picker();
    if (button.dataset.action === 'share') share();
  });

  chosen.length >= 2 ? comparison() : picker();
})();

