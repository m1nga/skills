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
assert(html.includes('aria-live="polite"'));
function run(raw,clipboardWorks=true){
 const elements=new Map();
 function el(id){if(!elements.has(id))elements.set(id,{id,value:({mood:'curious',platform:'codex',work:''})[id]||'',hidden:true,textContent:'',attrs:{},events:{},setAttribute(k,v){this.attrs[k]=v;},addEventListener(k,f){this.events[k]=f;},focus(){this.focused=true;},select(){this.selected=true;},click(){this.clicked=true;this.onclick?.();}});return elements.get(id);}
 const tabs=['angle','connection','idea'].map(x=>{const t=el('tab-'+x);t.dataset={mode:x};return t;});
 const downloads=[],blobs=[],copies=[];let readKey;
 const context=vm.createContext({document:{getElementById:el,querySelectorAll:()=>tabs,createElement:()=>{const a={click(){downloads.push(this);}};return a;}},localStorage:{getItem(key){readKey=key;return raw;}},navigator:{clipboard:{async writeText(s){if(!clipboardWorks)throw Error('unavailable');copies.push(s);}}},Blob:class {constructor(parts){blobs.push(parts.join(''));}},URL:{createObjectURL:()=> 'blob:test',revokeObjectURL(){}},setTimeout:f=>f()});
 vm.runInContext(script,context);return {el,tabs,downloads,blobs,copies,readKey};
}
const app=run(null);assert.equal(app.readKey,'breakinggap:v1');assert.equal(app.el('legacy').hidden,true);assert(app.el('question').textContent.includes('disappoint'));
app.el('tab-idea').click();assert.equal(app.el('tab-idea').attrs['aria-selected'],'true');assert.equal(app.el('tab-angle').tabIndex,-1);assert(app.el('starter').value.includes('do not invent my history'));assert(app.el('exampleLabel').textContent.includes('Invented intention'));assert(app.el('source').textContent.includes('Fictional supplied snippets'));assert(app.el('question').textContent.includes('might share a thread'));
app.el('another').click();assert(app.el('question').textContent.includes('field guide'));
let prevented=false;app.el('tab-idea').onkeydown({key:'ArrowRight',preventDefault(){prevented=true;}});assert(prevented);assert(app.el('tab-angle').focused);
app.el('work').value='A little garden';app.el('work').events.input();assert(app.el('starter').value.includes('A little garden'));app.el('platform').value='cc';app.el('platform').events.change();assert(app.el('starter').value.startsWith('/breakinggap'));
await app.el('copy').onclick();assert.equal(app.copies[0],app.el('starter').value);assert(app.el('feedback').textContent.includes('Copied'));
const fallback=run(null,false);await fallback.el('copy').onclick();assert(fallback.el('starter').selected);assert(fallback.el('starter').focused);assert(fallback.el('feedback').textContent.includes('Ctrl+C'));
for(const raw of ['{"session":{"draft":"keep me"}}','{malformed legacy data','']){const a=run(raw);assert.equal(a.el('legacy').hidden,false);a.el('exportLegacy').click();assert.equal(a.blobs[0],raw);assert.equal(a.downloads[0].download,'breakinggap-previous-session.txt');}
const svg=readFileSync(new URL('../assets/wordmark.svg',import.meta.url),'utf8');assert(svg.includes('<title id="title">BreakingGap</title>'));assert(!svg.includes('<image'));
console.log('Companion checks passed: modes, keyboard, starter, clipboard/fallback, untouched legacy export, offline/accessibility structure.');
