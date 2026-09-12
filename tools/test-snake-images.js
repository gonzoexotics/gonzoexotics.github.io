const fs = require('fs');
const vm = require('vm');

const context = { window: {}, console };
vm.createContext(context);
vm.runInContext(fs.readFileSync('snake-tools/assets/js/snake-data.js', 'utf8'), context);
const { species } = context.window.GonzoSnakeData;
const missing = [];

for (const item of species) {
  if (!item.image) missing.push(`${item.id}: image`);
  if (!item.imageCredit) missing.push(`${item.id}: imageCredit`);
  if (item.image && !item.image.startsWith('http') && !item.image.startsWith('assets/')) {
    missing.push(`${item.id}: invalid local path ${item.image}`);
  }
  if (item.image && item.image.startsWith('http') && !item.imageCreditUrl) {
    missing.push(`${item.id}: source URL`);
  }
}

if (missing.length) throw new Error(`Missing image data:\n${missing.join('\n')}`);
console.log(`PASS: all ${species.length} species have an image and a visible source credit.`);

