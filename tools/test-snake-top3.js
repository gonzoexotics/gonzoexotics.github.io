const fs = require('fs');
const vm = require('vm');

const context = { window: {}, console };
vm.createContext(context);
for (const file of ['assets/js/snake-data.js', 'assets/js/snake-engine.js']) {
  vm.runInContext(fs.readFileSync(`snake-tools/${file}`, 'utf8'), context, { filename: file });
}

const { species } = context.window.GonzoSnakeData;
const { rank } = context.window.GonzoSnakeEngine;
const experience = ['beginner', 'limited', 'experienced', 'advanced'];
const space = [90, 120, 150, 180, 240, 450];
const adultPlan = ['yes', 'later'];
const maintenance = ['basic', 'regular', 'daily'];
const prey = ['small', 'rats', 'large'];
let checked = 0;

for (const exp of experience) for (const room of space) for (const plan of adultPlan) {
  for (const care of maintenance) for (const food of prey) {
    const answers = {
      experience: exp, space: room, adultPlan: plan, size: 'any', handling: 'occasional',
      temperament: 'any', type: 'any', budget: 4500, climate: care === 'basic' ? 1 : 3,
      maintenance: care, prey: food, lifespan: 'any', cbb: 'yes', breeding: 'no', avoid: []
    };
    const result = rank(species, answers).slice(0, 3);
    if (result.length !== 3) throw new Error(`TOP 3 missing for ${JSON.stringify(answers)}: ${result.length}`);
    if (room <= 120 && result.some(item => item.species.id === 'python-bivittatus')) {
      throw new Error(`Python bivittatus returned for ${room} cm`);
    }
    checked += 1;
  }
}

console.log(`PASS: exactly three recommendations for ${checked} core answer profiles.`);
console.log('PASS: Python bivittatus never appears for 90 or 120 cm.');

