(function (root) {
  const levels = { beginner:0, limited:1, experienced:2, advanced:3 };
  if (typeof document !== 'undefined' && !document.getElementById('snake-tools-extra-css')) {
    const css = document.createElement('link');
    css.id = 'snake-tools-extra-css'; css.rel = 'stylesheet'; css.href = '../assets/css/snake-tools-extra.css';
    document.head.appendChild(css);
  }
  const weights = Object.freeze({ space:25, experience:15, climate:15, size:10, handling:10, prey:10, budget:7, type:5, activity:2, breeding:1 });
  const value = (v, ideal, fallback=.5) => ideal.includes(v) ? 1 : fallback;
  const preference = (species, a) => {
    const size = species.adultLengthMax <= 100 ? 'small' : species.adultLengthMax <= 170 ? 'medium' : species.adultLengthMax <= 280 ? 'large' : 'giant';
    const type = species.arborealLevel === 'wysoki' ? 'arboreal' : species.arborealLevel === 'średni' ? 'semi' : 'terrestrial';
    const handling = species.handlingPotential.includes('dobry') ? 'regular' : species.handlingPotential.includes('okazjonalny') ? 'occasional' : 'observation';
    const prey = species.largePreyRequired ? 'large' : species.typicalPrey.includes('szczury') ? 'rats' : 'small';
    return {
      space: Math.min(1, a.space / species.recommendedEnclosureLength),
      experience: Math.max(.1, 1 - Math.max(0, levels[species.hardExclusions.minExperience] - levels[a.experience]) * .45),
      climate: Math.max(.05, 1 - Math.max(0, species.climateDifficulty - a.climate) * .28),
      size: a.size === 'any' ? 1 : value(size, [a.size], .15),
      handling: a.handling === 'looks' ? 1 : value(handling, a.handling === 'regular' ? ['regular'] : a.handling === 'occasional' ? ['regular','occasional'] : ['observation'], .18),
      prey: value(prey, a.prey === 'small' ? ['small'] : a.prey === 'rats' ? ['small','rats'] : ['small','rats','large'], .1),
      budget: Math.min(1, a.budget / species.costFloor),
      type: a.type === 'any' ? 1 : value(type,[a.type],.35),
      activity: a.handling === 'observation' ? 1 : species.activityLevel === 'wysoka' ? .7 : 1,
      breeding: a.breeding === 'no' ? 1 : species.breedingDifficulty === 'zaawansowane planowanie' ? .5 : .8
    };
  };
  function scoreSpecies(species, a) {
    const blocks=[], penalties=[], why=[];
    if (a.space < Math.min(species.hardExclusions.minSpace, species.recommendedEnclosureLength)) blocks.push('planowana długość terrarium jest za mała dla rozsądnego docelowego planu');
    if (levels[a.experience] < levels[species.hardExclusions.minExperience] && species.hardExclusions.minExperience === 'advanced') blocks.push('poziom doświadczenia nie odpowiada wąskiemu marginesowi błędów tego gatunku');
    if (species.largePreyRequired && a.prey === 'small') blocks.push('nie akceptujesz wielkości karmówki, której gatunek może wymagać jako dorosły');
    if (a.adultPlan === 'later' && species.recommendedEnclosureLength >= 180) blocks.push('nie masz jeszcze pewnego planu na docelowe terrarium dużego gatunku');
    if (a.maintenance === 'basic' && species.climateDifficulty >= 3) blocks.push('deklarujesz zbyt mało czasu na kontrolę mikroklimatu tego gatunku');
    if (levels[a.experience] < levels[species.hardExclusions.minExperience]) penalties.push('doświadczenie jest niższe niż rozsądny punkt wejścia');
    if (species.climateDifficulty > a.climate + 1) penalties.push('deklarowana gotowość do kontroli mikroklimatu jest za niska');
    if (a.avoid.includes('microclimate') && species.climateDifficulty >= 3) penalties.push('chcesz unikać trudnego mikroklimatu');
    if (a.avoid.includes('large-enclosure') && species.recommendedEnclosureLength >= 180) penalties.push('chcesz unikać dużego terrarium');
    if (a.avoid.includes('large-snake') && species.adultLengthMax >= 180) penalties.push('chcesz unikać dużego węża');
    if (a.avoid.includes('large-prey') && species.largePreyRequired) penalties.push('chcesz unikać dużej karmówki');
    if (a.avoid.includes('observation') && species.handlingPotential.includes('obserwacyjny')) penalties.push('nie chcesz gatunku przede wszystkim do obserwacji');
    if (a.temperament === 'calm' && !species.handlingPotential.includes('dobry')) penalties.push('szukasz spokojniejszego gatunku niż sugeruje profil obsługi');
    if (a.cbb === 'unknown') penalties.push('przed zakupem trzeba najpierw zrozumieć różnicę między CBB a niezweryfikowanym pochodzeniem');
    if (a.lifespan === '15' && /20|25|30/.test(species.lifespan)) penalties.push('deklarowany horyzont opieki jest krótszy niż typowa długość życia gatunku');
    const pref=preference(species,a); let weighted=0; Object.entries(weights).forEach(([k,w])=>weighted += pref[k]*w);
    weighted -= penalties.length * 9;
    const potentialScore=Math.max(0,Math.min(100,Math.round(weighted)));
    if (blocks.length) weighted=0;
    if (a.space >= species.recommendedEnclosureLength) why.push('masz realną przestrzeń na docelowe terrarium');
    if (a.climate >= species.climateDifficulty) why.push('deklarujesz poziom kontroli mikroklimatu odpowiedni do jego wymagań');
    if (a.handling === 'observation' && species.handlingPotential.includes('obserwacyjny')) why.push('Twoje oczekiwania są bliższe obserwacji niż regularnemu handlingowi');
    if (a.handling !== 'observation' && species.handlingPotential.includes('dobry')) why.push('jego potencjał do spokojnej obsługi pasuje do Twoich oczekiwań');
    return { species, score:Math.max(0,Math.min(100,Math.round(weighted))), potentialScore, blocked:blocks.length>0, conditional:false, blocks, penalties, why, parts:pref };
  }
  function mayBeConditionalAlternative(result, answers) {
    const species=result.species;
    if (species.dataConfidence==='low') return false;
    if (species.hardExclusions.minExperience==='advanced' && levels[answers.experience] < levels.advanced) return false;
    if (species.largePreyRequired && answers.prey==='small') return false;
    if (species.recommendedEnclosureLength > Math.max(120, answers.space * 1.35)) return false;
    if (species.adultLengthMax >= 300 && answers.space < 300) return false;
    if (answers.maintenance==='basic' && species.climateDifficulty >= 3) return false;
    if (answers.adultPlan==='later' && species.recommendedEnclosureLength >= 180) return false;
    return true;
  }
  function rank(species, answers) {
    const all=species.map(s=>scoreSpecies(s,answers)).filter(r=>r.species.dataConfidence!=='low');
    const safe=all.filter(r=>!r.blocked).sort((a,b)=>b.score-a.score);
    if (safe.length>=3) return safe;
    const conditional=all
      .filter(r=>r.blocked && mayBeConditionalAlternative(r,answers))
      .sort((a,b)=>a.blocks.length-b.blocks.length || b.potentialScore-a.potentialScore)
      .map(r=>({...r,score:Math.max(1,r.potentialScore-r.blocks.length*12),blocked:false,conditional:true}));
    return safe.concat(conditional).slice(0,Math.max(3,safe.length));
  }
  function explanation(r) {
    if (r.conditional) return `To propozycja warunkowa. Przed wyborem musisz zmienić ten element planu: ${r.blocks.join('; ')}.`;
    return r.why.length ? `Ten gatunek wypada wysoko, ponieważ ${r.why.slice(0,2).join(' oraz ')}.` : 'Wynik opiera się na zgodności miejsca, doświadczenia, klimatu i oczekiwań.';
  }
  root.GonzoSnakeEngine=Object.freeze({weights,scoreSpecies,rank,explanation,levels});
})(window);

