const fs = require('fs');
const vm = require('vm');

const root = process.cwd();
const html = fs.readFileSync('porownaj-weze/index.html', 'utf8');
const context = { window: {} };
vm.createContext(context);
vm.runInContext(fs.readFileSync('assets/js/snake-data.js', 'utf8'), context);

const { species } = context.window.GonzoSnakeData;
const itemListJson = [...html.matchAll(/<script type="application\/ld\+json">\s*([\s\S]*?)\s*<\/script>/g)]
  .map(match => JSON.parse(match[1]))
  .find(item => item['@type'] === 'ItemList');
const profiles = (html.match(/class="species-profile(?:\s|"|--)/g) || []).length;
const indexLinks = (html.match(/<a href="#[^"]+">/g) || []).length;
const missingImages = species.filter(item => !fs.existsSync(`${root}/${item.image}`));

if (species.length !== 23) throw new Error(`Expected 23 data profiles, got ${species.length}.`);
if (profiles !== 23) throw new Error(`Expected 23 static profiles, got ${profiles}.`);
if (!itemListJson || itemListJson.numberOfItems !== 23 || itemListJson.itemListElement.length !== 23) throw new Error('ItemList must list all 23 profiles.');
if (indexLinks < 23) throw new Error(`Expected at least 23 fragment links, got ${indexLinks}.`);
if (missingImages.length) throw new Error(`Missing local images: ${missingImages.map(item => item.image).join(', ')}`);
console.log('PASS: data, static library, structured ItemList and local photographs agree on 23 species.');
