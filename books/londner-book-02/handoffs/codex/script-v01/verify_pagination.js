const fs=require('fs'),vm=require('vm'),assert=require('assert'),path=require('path');
const root=__dirname;
const html=fs.readFileSync(path.join(root,'book2-reader.html'),'utf8');
const js=html.match(/<script>([\s\S]*?)<\/script>/)[1];
new vm.Script(js);
const elements=new Map();
function element(id){if(!elements.has(id))elements.set(id,{innerHTML:'',value:'',disabled:false,textContent:'',classList:{toggle(){}}});return elements.get(id);}
const ctx={document:{body:{dataset:{default:'reader',directions:'on'}},getElementById:element,querySelectorAll:()=>[],addEventListener(){}},window:{addEventListener(){}},location:{hash:''}};
vm.createContext(ctx);vm.runInContext(js,ctx);
const visible=()=>[...element('spread').innerHTML.matchAll(/<span>(\d+) \/ 64<\/span>/g)].map(m=>Number(m[1]));
assert.deepStrictEqual(visible(),[1]);element('next').onclick();assert.deepStrictEqual(visible(),[2,3]);element('previous').onclick();assert.deepStrictEqual(visible(),[1]);
const book=JSON.parse(fs.readFileSync(path.join(root,'book2-script.json'),'utf8'));
for(const t of book.page_turns){ctx.selectPage(t.setup);const before=visible();ctx.selectPage(t.reveal);const after=visible();assert(before.includes(t.setup));assert(!before.includes(t.reveal));assert(after.includes(t.reveal));assert(before.every(n=>!after.includes(n)));}
ctx.selectPage(999);assert.deepStrictEqual(visible(),[64]);assert(element('next').disabled);ctx.location.hash='#read-0';ctx.route();assert.deepStrictEqual(visible(),[1]);ctx.location.hash='#read-999';ctx.route();assert.deepStrictEqual(visible(),[64]);
element('spreadToggle').onclick({target:element('spreadToggle')});ctx.selectPage(23);assert.deepStrictEqual(visible(),[23]);
const he=element('spread').innerHTML;element('languageToggle').onclick({target:element('languageToggle')});const en=element('spread').innerHTML;assert(en!==he);assert(en.includes('If you wish, come with me.'));assert(en.includes('dir="ltr"'));element('languageToggle').onclick({target:element('languageToggle')});assert(element('spread').innerHTML.includes('תבואו איתי'));
element('directionToggle').onclick({target:element('directionToggle')});assert.strictEqual(ctx.document.body.dataset.directions,'off');
console.log(JSON.stringify({javascript_syntax:'passed',actual_navigation_functions:'passed with DOM stub',page_turns:book.page_turns.length,language_toggle:'passed',directions_toggle:'passed',browser_visual_qa:'not performed'}));
