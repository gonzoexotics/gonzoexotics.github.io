(function () {
  const app = document.getElementById('quiz-app');
  if (!app || !window.GonzoSnakeData || !window.GonzoSnakeEngine) return;

  const { species } = window.GonzoSnakeData;
  const { rank, scoreSpecies, explanation } = window.GonzoSnakeEngine;
  const makeQuestion = (key, title, options, help = '', multiple = false) => ({ key, title, options, help, multiple });
  const questions = [
    makeQuestion('experience', 'Jak oceniasz doświadczenie?', [['beginner', 'To mój pierwszy wąż'], ['limited', 'Mam podstawy'], ['experienced', 'Prowadziłem/am kilka gatunków'], ['advanced', 'Mam duże doświadczenie']], 'Wybierz uczciwie — to filtr bezpieczeństwa.'),
    makeQuestion('space', 'Jaka jest realna długość miejsca na docelowe terrarium?', [[90, '90 cm'], [120, '120 cm'], [150, '150 cm'], [180, '180 cm'], [240, '240 cm'], [450, 'duża zabudowa / pomieszczenie']], 'Nie „kiedyś”. Wybierz miejsce, które będzie dostępne dla dorosłego węża.'),
    makeQuestion('adultPlan', 'Czy docelowe terrarium dla dorosłego osobnika jest pewne przed zakupem?', [['yes', 'tak, mam konkretny plan'], ['later', 'nie, liczę że ogarnę to później']]),
    makeQuestion('size', 'Jaki rozmiar dorosłego węża chcesz?', [['small', 'mały'], ['medium', 'średni'], ['large', 'duży'], ['giant', 'bardzo duży'], ['any', 'bez preferencji']]),
    makeQuestion('handling', 'Czego oczekujesz od kontaktu?', [['regular', 'spokojny handling od czasu do czasu'], ['occasional', 'głównie obserwacja, kontakt okazjonalny'], ['observation', 'gatunek przede wszystkim do obserwacji'], ['looks', 'wygląd; dopasuję opiekę do gatunku']]),
    makeQuestion('temperament', 'Jak podchodzisz do szybkiego lub defensywnego zachowania?', [['calm', 'wolę możliwie spokojny gatunek'], ['active', 'akceptuję aktywne, szybsze zwierzę'], ['any', 'sprawdzę temperament konkretnego osobnika']]),
    makeQuestion('type', 'Jakie środowisko najbardziej Cię interesuje?', [['terrestrial', 'naziemne'], ['semi', 'półnadrzewne'], ['arboreal', 'nadrzewne'], ['any', 'bez znaczenia']]),
    makeQuestion('budget', 'Jaki jest budżet na węża i kompletne przygotowanie?', [[1500, 'do 1 500 zł'], [2500, 'około 2 500 zł'], [4500, 'około 4 500 zł'], [7000, 'około 7 000 zł'], [15000, '15 000 zł lub więcej']], 'Terrarium i termostat są ważniejsze niż oszczędność na starcie.'),
    makeQuestion('climate', 'Jaką gotowość masz do kontroli mikroklimatu?', [[1, 'wolę prosty, wybaczający mikroklimat'], [2, 'dopilnuję stabilnych parametrów'], [3, 'akceptuję regularne pomiary i korekty'], [4, 'mam doświadczenie z wymagającym mikroklimatem']]),
    makeQuestion('maintenance', 'Ile rutynowej pracy możesz wykonywać co tydzień?', [['basic', 'woda, sprzątanie i podstawowa kontrola'], ['regular', 'regularny serwis i kontrola parametrów'], ['daily', 'codzienna obserwacja jest w porządku']]),
    makeQuestion('prey', 'Jaką wielkość karmówki akceptujesz docelowo?', [['small', 'tylko małe gryzonie'], ['rats', 'myszy i szczury'], ['large', 'również dużą karmówkę']]),
    makeQuestion('lifespan', 'Na jaki horyzont opieki jesteś gotowy/gotowa?', [['15', 'około 10–15 lat'], ['25', '20 lat lub więcej'], ['any', 'na długoletnią opiekę']]),
    makeQuestion('cbb', 'Czy wybierasz wyłącznie zdrowe CBB od sprawdzonego źródła?', [['yes', 'tak — CBB i dokumentacja'], ['wait', 'tak, nawet jeśli trzeba poczekać'], ['unknown', 'nie wiem jeszcze, co to oznacza']]),
    makeQuestion('breeding', 'Czy rozmnażanie jest celem?', [['no', 'nie, interesuje mnie odpowiedzialna opieka'], ['maybe', 'może kiedyś'], ['yes', 'tak, świadomie planuję hodowlę']]),
    makeQuestion('avoid', 'Czego chcesz unikać?', [['microclimate', 'trudnego mikroklimatu'], ['large-enclosure', 'bardzo dużego terrarium'], ['large-snake', 'bardzo dużego węża'], ['large-prey', 'dużej karmówki'], ['observation', 'gatunku głównie do obserwacji']], 'Możesz wybrać kilka odpowiedzi lub pominąć.', true)
  ];

  let step = -1;
  let answers = {};
  const escapeHtml = value => String(value).replace(/[&<>"']/g, character => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[character]));
  const photoStyle = item => item.image ? ` style="background-image:linear-gradient(180deg,transparent 25%,rgba(5,8,7,.82)),url('${escapeHtml(item.image.startsWith('http') ? item.image : '../' + item.image)}')"` : '';
  const photoCredit = item => item.imageCredit ? `<p class="photo-credit">${item.imageCreditUrl ? `<a href="${escapeHtml(item.imageCreditUrl)}" target="_blank" rel="noopener noreferrer">${escapeHtml(item.imageCredit)}</a>` : escapeHtml(item.imageCredit)}</p>` : '';

  function renderStart() {
    app.innerHTML = '<article class="quiz-card quiz-start"><p class="snake-eyebrow">15 PYTAŃ • BEZ LOGOWANIA</p><h2>Najpierw warunki. Potem gatunek.</h2><p>Po odpowiedziach pokażemy zawsze trzy możliwe kierunki. Jeśli któryś wymaga zmiany planu, zaznaczymy to wprost.</p><button class="snake-button" data-action="start">Rozpocznij quiz</button></article>';
  }

  function renderQuestion() {
    const question = questions[step];
    const selected = answers[question.key];
    const options = question.options.map(([value, label]) => {
      const active = question.multiple ? (selected || []).includes(value) : selected === value;
      return `<button class="answer-option${active ? ' selected' : ''}" data-value="${escapeHtml(value)}" aria-pressed="${active}"><span>${escapeHtml(label)}</span><b>${active ? '✓' : '›'}</b></button>`;
    }).join('');
    app.innerHTML = `<article class="quiz-card"><p class="quiz-progress">Pytanie ${step + 1} z ${questions.length}</p><div class="progress-track"><span style="width:${(step + 1) / questions.length * 100}%"></span></div><h2>${escapeHtml(question.title)}</h2>${question.help ? `<p class="quiz-help">${escapeHtml(question.help)}</p>` : ''}<div class="answer-options">${options}</div><div class="quiz-actions"><button class="snake-button secondary" data-action="back" ${step ? '' : 'disabled'}>Wstecz</button><button class="snake-button" data-action="next" ${(!question.multiple && !selected) ? 'disabled' : ''}>${step === questions.length - 1 ? 'Pokaż moje TOP 3' : 'Dalej'}</button></div></article>`;
  }

  function renderCard(result, index) {
    const item = result.species;
    const normalLabels = ['Najbliższe dopasowanie', 'Druga propozycja', 'Trzecia propozycja'];
    const label = result.conditional ? `Propozycja warunkowa nr ${index + 1}` : normalLabels[index];
    return `<article class="result-card${result.conditional ? ' conditional-result' : ''}"><div class="snake-photo"${photoStyle(item)}><span>Propozycja ${index + 1} z 3</span></div><div class="result-copy"><p class="result-rank">${label} • ${result.score}/100</p><h2><em>${escapeHtml(item.scientificName)}</em><br>${escapeHtml(item.commonName)}</h2>${photoCredit(item)}<p>${escapeHtml(item.shortDescription)}</p><p class="result-why"><strong>${result.conditional ? 'Co trzeba zmienić:' : 'Dlaczego może pasować:'}</strong> ${escapeHtml(explanation(result))}</p><dl class="quick-facts"><div><dt>Docelowe terrarium</dt><dd>${escapeHtml(item.recommendedEnclosure)}</dd></div><div><dt>Trudność</dt><dd>${escapeHtml(item.experienceLevel)}</dd></div><div><dt>Koszt startowy</dt><dd>${escapeHtml(item.startupCost)}</dd></div></dl><a class="text-link" href="../porownaj-weze/?species=${encodeURIComponent(item.id)}">Porównaj ten gatunek</a></div></article>`;
  }

  function renderResults() {
    const top = rank(species, answers).slice(0, 3);
    const topIds = new Set(top.map(result => result.species.id));
    const rejected = species.map(item => scoreSpecies(item, answers))
      .filter(result => !topIds.has(result.species.id) && (result.blocked || result.penalties.length > 1))
      .sort((a, b) => b.potentialScore - a.potentialScore)
      .slice(0, 3);

    if (top.length !== 3) {
      app.innerHTML = '<article class="quiz-card"><h2>Nie udało się zbudować trzech uczciwych propozycji</h2><p>Zmień przynajmniej jeden warunek dotyczący miejsca, doświadczenia albo karmówki.</p><button class="snake-button" data-action="reset">Zmień odpowiedzi</button></article>';
      return;
    }

    const ids = top.map(result => result.species.id).join(',');
    app.innerHTML = `<section class="result-intro"><p class="snake-eyebrow">TWOJE TOP 3</p><h2>Trzy propozycje dopasowane do odpowiedzi</h2><p>Najlepiej dopasowany gatunek jest pierwszy. Pozostałe dwie karty pokazują bliskie alternatywy. Gdy wymagana jest zmiana warunków, karta jest wyraźnie oznaczona jako warunkowa.</p></section><div class="result-list">${top.map(renderCard).join('')}</div>${rejected.length ? `<aside class="why-not"><h2>Czego nie proponujemy przy tych odpowiedziach</h2>${rejected.map(result => `<p><strong>${escapeHtml(result.species.commonName)}:</strong> ${escapeHtml(result.blocks[0] || result.penalties[0])}.</p>`).join('')}</aside>` : ''}<div class="result-actions"><a class="snake-button" href="../porownaj-weze/?species=${encodeURIComponent(ids)}">Porównaj moje TOP 3</a><button class="snake-button secondary" data-action="reset">Zmień odpowiedzi</button></div><p class="tool-note">Wynik jest punktem startu. Przed zakupem sprawdź zdrowie, CBB, dokumentację oraz przygotuj docelowe terrarium.</p>`;
  }

  app.addEventListener('click', event => {
    const button = event.target.closest('button');
    if (!button) return;
    const action = button.dataset.action;
    if (action === 'start') { step = 0; renderQuestion(); return; }
    if (action === 'back') { step = Math.max(0, step - 1); renderQuestion(); return; }
    if (action === 'next') { step === questions.length - 1 ? renderResults() : (step += 1, renderQuestion()); return; }
    if (action === 'reset') { step = -1; answers = {}; renderStart(); return; }

    const question = questions[step];
    if (!question || button.dataset.value === undefined) return;
    const raw = button.dataset.value;
    const value = ['space', 'budget', 'climate'].includes(question.key) ? Number(raw) : raw;
    if (question.multiple) {
      const previous = answers[question.key] || [];
      answers[question.key] = previous.includes(value) ? previous.filter(item => item !== value) : [...previous, value];
    } else {
      answers[question.key] = value;
    }
    renderQuestion();
  });

  renderStart();
})();

