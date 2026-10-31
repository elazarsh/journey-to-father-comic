const fs=require('fs'),vm=require('vm'),assert=require('assert');
const path=require('path');
const root=__dirname;
const html=fs.readFileSync(path.join(root,'book1-reader.html'),'utf8');
const js=html.match(/<script>([\s\S]*?)<\/script>/)[1];
new vm.Script(js);
// Exercise the actual reader functions without claiming a browser render.
const elements=new Map();
function element(id){if(!elements.has(id))elements.set(id,{innerHTML:'',value:'',disabled:false,textContent:'',classList:{toggle(){}}});return elements.get(id);}
const context={document:{body:{dataset:{default:'reader',art:'on'}},images:[],getElementById:element,querySelectorAll:()=>[],addEventListener(){}},window:{addEventListener(){}},location:{hash:''}};
vm.createContext(context);vm.runInContext(js,context);
function visible(){return [...element('spread').innerHTML.matchAll(/<span>(\d+) \/ 48<\/span>/g)].map(m=>Number(m[1]));}
assert.deepStrictEqual(visible(),[1]);
element('next').onclick();assert.deepStrictEqual(visible(),[2,3]);
element('previous').onclick();assert.deepStrictEqual(visible(),[1]);
const book=JSON.parse(fs.readFileSync(path.join(root,'book1-script.json'),'utf8'));
for(const t of book.page_turns){context.selectPage(t.setup);const before=visible();context.selectPage(t.reveal);const after=visible();assert(before.includes(t.setup));assert(!before.includes(t.reveal));assert(after.includes(t.reveal));assert(before.every(p=>!after.includes(p)));}
context.selectPage(48);assert.deepStrictEqual(visible(),[48]);assert(element('next').disabled);
context.selectPage(999);assert.deepStrictEqual(visible(),[48]);
context.location.hash='#read-0';context.route();assert.deepStrictEqual(visible(),[1]);
context.location.hash='#read-999';context.route();assert.deepStrictEqual(visible(),[48]);
element('spreadToggle').onclick({target:element('spreadToggle')});context.selectPage(11);assert.deepStrictEqual(visible(),[11]);
console.log(JSON.stringify({javascript:'passed',actual_navigation_functions:'passed',provisional_page_turn_pairs:book.page_turns.length,browser_visual_qa:'not performed'}));
