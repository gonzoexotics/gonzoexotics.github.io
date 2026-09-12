const fs = require('fs');
const vm = require('vm');

let clickHandler;
const app = {
  innerHTML: '',
  addEventListener(type, handler) { if (type === 'click') clickHandler = handler; }
};
const context = { window: {}, console };
vm.createContext(context);
for (const file of ['assets/js/snake-data.js', 'assets/js/snake-engine.js']) {
  vm.runInContext(fs.readFileSync(`snake-tools/${file}`, 'utf8'), context, { filename: file });
}
context.document = { getElementById(id) { return id === 'quiz-app' ? app : null; } };
vm.runInContext(fs.readFileSync('snake-tools/assets/js/snake-quiz-v2.js', 'utf8'), context, { filename: 'snake-quiz-v2.js' });

const click = dataset => clickHandler({ target: { closest: () => ({ dataset }) } });
click({ action: 'start' });
const answers = ['beginner', '90', 'yes', 'small', 'occasional', 'calm', 'terrestrial', '1500', '1', 'basic', 'small', '15', 'yes', 'no'];
for (const value of answers) {
  click({ value });
  click({ action: 'next' });
}
click({ action: 'next' });

const cards = (app.innerHTML.match(/class="result-card/g) || []).length;
if (cards !== 3) throw new Error(`Rendered ${cards} result cards instead of 3.`);
for (const number of [1, 2, 3]) {
  if (!app.innerHTML.includes(`Propozycja ${number} z 3`)) throw new Error(`Missing visible label for proposal ${number}.`);
}
if (app.innerHTML.includes('Pyton birmański')) throw new Error('Python bivittatus appeared for a 90 cm profile.');
console.log('PASS: constrained quiz profile renders three separately labelled cards.');

