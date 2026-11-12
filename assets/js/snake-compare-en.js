(function () {
  const app = document.getElementById('compare-app');
  if (!app || !window.GonzoSnakeData) return;

  const species = window.GonzoSnakeData.species.map(item => ({ ...item, ...(window.GonzoSnakeEnglish?.[item.id] || {}) }));
  const params = new URLSearchParams(location.search);
  let chosen = (params.get('species') || '').split(',').filter(id => species.some(item => item.id === id)).slice(0, 3);
  const escapeHtml = value => String(value).replace(/[&<>"']/g, character => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[character]));
  const imageUrl = item => item.image.startsWith('http') ? item.image : `/${item.image}`;
  const image = (item, className, alt = '') => `<span class="${className}"><img src="${escapeHtml(imageUrl(item))}" alt="${escapeHtml(alt)}" decoding="async" referrerpolicy="no-referrer" width="164" height="140"></span>`;
  const credit = item => item.imageCredit ? `<p class="photo-credit">${item.imageCreditUrl ? `<a href="${escapeHtml(item.imageCreditUrl)}" target="_blank" rel="noopener noreferrer">${escapeHtml(item.imageCredit)}</a>` : escapeHtml(item.imageCredit)}</p>` : '';
  const section = (title, content) => `<details open><summary>${title}</summary><div>${content}</div></details>`;

  function card(item) {
    return `<article class="compare-card"><div class="snake-photo"><img src="${escapeHtml(imageUrl(item))}" alt="${escapeHtml(`${item.commonName} (${item.scientificName})`)}" loading="lazy" decoding="async" referrerpolicy="no-referrer"><span>Species photograph</span></div><div class="compare-card-copy"><h2><em>${escapeHtml(item.scientificName)}</em><br>${escapeHtml(item.commonName)}</h2>${credit(item)}<p>${escapeHtml(item.shortDescription)}</p>${section('Enclosure and size', `<p><strong>Adult length:</strong> ${item.adultLengthMin}–${item.adultLengthMax} cm</p><p><strong>Recommended enclosure:</strong> ${escapeHtml(item.recommendedEnclosure)}</p><p><strong>Type:</strong> ${escapeHtml(item.enclosureType)}</p>`)}${section('Microclimate', `<p><strong>Temperature:</strong> ${escapeHtml(item.temperatureModel)}</p><p><strong>Humidity:</strong> ${escapeHtml(item.humidityModel)}</p><p><strong>Ventilation:</strong> ${escapeHtml(item.ventilationImportance)}</p>`)}${section('Daily care', `<p><strong>Activity:</strong> ${escapeHtml(item.activityLevel)} (${escapeHtml(item.activityPeriod)})</p><p><strong>Handling:</strong> ${escapeHtml(item.handlingPotential)}</p><p><strong>Feeding:</strong> ${escapeHtml(item.typicalPrey)}</p><p><strong>Initial cost:</strong> ${escapeHtml(item.startupCost)}</p>`)}${section('Benefits and challenges', `<p><strong>Benefits:</strong> ${escapeHtml(item.advantages.join('; '))}</p><p><strong>Challenges:</strong> ${escapeHtml(item.challenges.join('; '))}</p>`)}<p class="legal-note"><strong>Legal considerations:</strong> ${escapeHtml(item.legalNotes)}</p></div></article>`;
  }

  function picker() {
    const choices = species.map(item => `<button type="button" class="species-choice${chosen.includes(item.id) ? ' selected' : ''}" data-id="${escapeHtml(item.id)}" aria-pressed="${chosen.includes(item.id)}">${image(item, 'species-choice-photo')}<span class="species-choice-copy"><em>${escapeHtml(item.scientificName)}</em><span>${escapeHtml(item.commonName)}</span></span></button>`).join('');
    app.innerHTML = `<section class="compare-picker"><h2>Choose 2 or 3 species</h2><p>Each species has its own photograph. Select the cards you want to compare.</p><div class="species-picker" aria-label="Species list">${choices}</div><div class="quiz-actions"><button class="snake-button" type="button" data-action="compare" ${chosen.length < 2 ? 'disabled' : ''}>Compare selected (${chosen.length}/3)</button><button class="snake-button secondary" type="button" data-action="clear" ${chosen.length ? '' : 'disabled'}>Clear</button></div></section>`;
  }

  function comparison() {
    const selected = chosen.map(id => species.find(item => item.id === id));
    app.innerHTML = `<section class="comparison-intro"><p class="snake-eyebrow">SPECIES COMPARISON</p><h2>Differences that matter in husbandry</h2><p>The parameters are a practical starting point. Do not automatically transfer settings between species, especially between <em>Corallus caninus</em> a <em>Morelia viridis</em>.</p><button class="text-link" type="button" data-action="edit">Change selection</button></section><div class="comparison-grid">${selected.map(card).join('')}</div><aside class="why-not"><h2>How to read this comparison</h2><p>The greatest differences usually concern the eventual size of the enclosure, the margin for error in microclimate, prey and whether the species is best observed or can be handled occasionally.</p></aside><div class="result-actions"><button class="snake-button secondary" type="button" data-action="share">Share comparison</button><a class="snake-button secondary" href="/jaki-waz-dla-ciebie/">Open quiz (Polish)</a></div>`;
  }

  async function share() {
    try {
      const url = location.href;
      if (navigator.share) await navigator.share({ title: 'Snake comparison — Gonzo Exotics', url });
      else if (navigator.clipboard) { await navigator.clipboard.writeText(url); alert('Comparison link copied.'); }
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
