import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const html=readFileSync(new URL('../assets/companion.html',import.meta.url),'utf8');
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
assert(!/(?:src|href)=["']https?:/i.test(html));
assert(!/\b(?:fetch|XMLHttpRequest|WebSocket)\s*\(/.test(script));
assert(!/localStorage\.(?:setItem|removeItem|clear)/.test(script));
assert(html.includes('prefers-reduced-motion:reduce'));
assert(html.includes('not connected to your chats'));
assert(html.includes('fictional examples'));
assert(html.includes('cannot open a chat'));
assert(!/setInterval|requestAnimationFrame/.test(script));
assert(html.includes('aria-live="polite"'));
function run(raw,clipboardWorks=true){
 const elements=new Map();
 function el(id){if(!elements.has(id))elements.set(id,{id,value:({mood:'curious',platform:'codex',work:''})[id]||'',hidden:true,textContent:'',attrs:{},events:{},setAttribute(k,v){this.attrs[k]=v;},addEventListener(k,f){this.events[k]=f;},replaceChildren(...children){this.children=children;},focus(){this.focused=true;},select(){this.selected=true;},click(){this.clicked=true;this.onclick?.();}});return elements.get(id);}
 const tabs=['angle','connection','idea'].map(x=>{const t=el('tab-'+x);t.dataset={mode:x};return t;});
 const downloads=[],blobs=[],copies=[];let readKey;
 const context=vm.createContext({document:{getElementById:el,querySelectorAll:()=>tabs,createElement:tag=>{const a={tag,textContent:'',click(){downloads.push(this);}};return a;}},localStorage:{getItem(key){readKey=key;return raw;}},navigator:{clipboard:{async writeText(s){if(!clipboardWorks)throw Error('unavailable');copies.push(s);}}},Blob:class {constructor(parts){blobs.push(parts.join(''));}},URL:{createObjectURL:()=> 'blob:test',revokeObjectURL(){}},setTimeout:f=>f()});
 vm.runInContext(script,context);return {el,tabs,downloads,blobs,copies,readKey};
}
const app=run(null);assert.equal(app.readKey,'breakinggap:v1');assert.equal(app.el('legacy').hidden,true);
const seen=new Set();
for(const tab of app.tabs){
 tab.click();seen.add(app.el('question').textContent);
 assert.equal(tab.attrs['aria-selected'],'true');assert.equal(tab.tabIndex,0);
 assert.equal(app.el('questions').children.length,3);
 assert(app.el('questions').children.every(q=>q.tag==='li'&&q.textContent.endsWith('?')));
 assert(app.el('source').textContent.startsWith('Fictional'));
 assert(app.el('deeper').textContent.startsWith('In this fictional example'));
 assert(app.el('handoff').textContent.includes('separate chat'));
 assert(app.el('invitation').textContent.includes('three minutes'));
 assert.equal(app.el('example').attrs['aria-labelledby'],tab.id);
}
assert.equal(seen.size,3);assert.equal(app.el('tab-angle').tabIndex,-1);
app.el('another').click();assert.equal(app.el('tab-angle').attrs['aria-selected'],'true');
let prevented=false;app.el('tab-angle').onkeydown({key:'ArrowLeft',preventDefault(){prevented=true;}});assert(prevented);assert(app.el('tab-idea').focused);
app.el('tab-idea').onkeydown({key:'Home',preventDefault(){}});assert(app.el('tab-angle').focused);
app.el('tab-angle').onkeydown({key:'End',preventDefault(){}});assert(app.el('tab-idea').focused);
app.el('work').value='<script>A little garden</script>';app.el('work').events.input();assert(app.el('starter').value.includes('<script>A little garden</script>'));
assert(app.el('starter').value.startsWith('$breakinggap'));
app.el('platform').value='cc';app.el('platform').events.change();assert(app.el('starter').value.startsWith('/breakinggap'));
assert(app.el('starter').value.includes('two or three broad, open questions'));
assert(app.el('starter').value.includes('After any reflection'));
assert(app.el('starter').value.includes('No timer or automatic follow-up'));
app.el('starter').value='My edited starter';
await app.el('copy').onclick();assert.equal(app.copies[0],app.el('starter').value);assert(app.el('feedback').textContent.includes('Copied'));
const fallback=run(null,false);await fallback.el('copy').onclick();assert(fallback.el('starter').selected);assert(fallback.el('starter').focused);assert(fallback.el('feedback').textContent.includes('Ctrl+C'));
for(const raw of ['{"session":{"draft":"keep me"}}','{malformed legacy data','']){const a=run(raw);assert.equal(a.el('legacy').hidden,false);a.el('exportLegacy').click();assert.equal(a.blobs[0],raw);assert.equal(a.downloads[0].download,'breakinggap-previous-session.txt');}
const svg=readFileSync(new URL('../assets/wordmark.svg',import.meta.url),'utf8');assert(svg.includes('<title id="title">BreakingGap</title>'));assert(!svg.includes('<image'));
console.log('Companion checks passed: three complete fictional examples, keyboard navigation, editable starter, clipboard/fallback, untouched legacy export, offline/accessibility structure.');
