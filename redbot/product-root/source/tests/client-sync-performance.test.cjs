const {test}=require('node:test'),assert=require('node:assert/strict'),vm=require('node:vm'),fs=require('node:fs'),path=require('node:path');
const source=fs.readFileSync(path.join(__dirname,'../app/client.js'),'utf8'),C=require('../app/core.js');
const section=(a,b)=>source.slice(source.indexOf(a),source.indexOf(b));
function harness(){
 const h=vm.createContext({C,JSON});
 vm.runInContext(`let libraryPage=null,scope='A',data={items:[{id:'one',title:'One'},{id:'two',title:'Two'}],annotations:{one:{note:'My note'}},remoteCursor:'prior',scan:{at:'today'}},tab='library',saved=0,painted=0,requests=[],resolve;
 const libraryKey=()=>scope,$=()=>({}),cards=()=>painted++,updateProgress=()=>{},render=()=>{},refreshDetail=()=>{};
 async function save(){saved++;}async function api(url){requests.push(url);return new Promise(r=>resolve=r);}
 ${section('  async function loadLibrary()','  function cancelSearch()')}
 globalThis.run=loadLibrary;globalThis.reply=x=>resolve(x);globalThis.switchAccount=()=>{scope='B';data={items:[{id:'other',title:'Other account'}],annotations:{}};};globalThis.state=()=>({data,saved,painted,requests});`,h);return h;
}
test('delta changes one source without losing other saves or personal notes',async()=>{
 const h=harness(),p=h.run();h.reply({items:[{id:'one',title:'Updated',description:'New source text'}],mode:'delta',cursor:'next',scan:{at:'today'}});await p;
 const s=h.state();assert.equal(s.requests[0],'/api/library?paged=1&cursor=prior');assert.deepEqual(Array.from(s.data.items,x=>x.id),['one','two']);assert.equal(s.data.items[0].title,'Updated');assert.equal(s.data.annotations.one.note,'My note');assert.equal(s.data.remoteCursor,'next');assert.equal(s.saved,1);
});
test('empty delta avoids rewriting and repainting the entire unchanged library',async()=>{
 const h=harness(),p=h.run();h.reply({items:[],mode:'delta',cursor:'prior',scan:{at:'today'}});await p;
 assert.equal(h.state().saved,0);assert.equal(h.state().painted,0);assert.equal(h.state().data.items.length,2);
});
test('late response from a former account cannot enter a newly connected library',async()=>{
 const h=harness(),p=h.run();h.switchAccount();h.reply({items:[{id:'one',title:'Private old account'}],cursor:'old-cursor',scan:{}});await p;
 assert.equal(h.state().data.items[0].id,'other');assert.equal(h.state().data.remoteCursor,undefined);assert.equal(h.state().saved,0);
});
test('cached app shell opens without waiting for a slow network; API/config/version bypass cache',async()=>{
 const handlers={},saved={cached:true};let fetches=0,response;
 const h=vm.createContext({URL,Request,location:{origin:'https://redbot.example'},registration:{scope:'https://redbot.example/app/'},self:{addEventListener:(n,f)=>handlers[n]=f},caches:{open:async()=>({match:async()=>saved})},fetch:()=>{fetches++;return new Promise(()=>{});}});
 vm.runInContext(fs.readFileSync(path.join(__dirname,'../app/sw.js'),'utf8'),h);
 handlers.fetch({request:new Request('https://redbot.example/app/client.js?v=1.9.7'),respondWith:p=>response=p});assert.equal(await response,saved);assert.equal(fetches,0);
 for(const url of ['https://redbot.example/app/version.json','https://redbot.example/app/connection.json','https://sync.example/api/library']){
  let intercepted=false;handlers.fetch({request:new Request(url),respondWith:()=>intercepted=true});assert.equal(intercepted,false);
 }
});
test('update reload waits until the replacement cached application activates',async()=>{
 let listener;const worker={state:'installed',addEventListener:(n,f)=>listener=f,removeEventListener:()=>{}};
 const h=vm.createContext({navigator:{serviceWorker:{getRegistration:async()=>({update:async()=>{},waiting:worker})}},setTimeout,clearTimeout,worker});
 vm.runInContext(`let detailId=null,reloads=0,saved=0;const $=()=>null,t=x=>x,notify=()=>{};async function save(){saved++;return true;}const location={reload:()=>reloads++};
 ${section('  async function reloadUpdatedApp()','  function timecode(')}
 globalThis.run=reloadUpdatedApp;globalThis.state=()=>({reloads,saved});`,h);
 const p=h.run();await new Promise(resolve=>setImmediate(resolve));assert.equal(h.state().saved,1);assert.equal(h.state().reloads,0);
 worker.state='activated';listener();await p;assert.equal(h.state().reloads,1);
});

test('partial pages render now but advance the completed cursor only after the last page',async()=>{
 const h=harness(),first=h.run();h.reply({items:[{id:'one',title:'First page',description:'Readable now'}],cursor:'target',next:'page-two',scan:{at:'today'}});
 assert.equal(await first,false);assert.equal(h.state().data.items[0].title,'First page');assert.equal(h.state().data.remoteCursor,'prior');
 const last=h.run();assert.equal(h.state().requests[1],'/api/library?paged=1&cursor=prior&page=page-two');h.reply({items:[{id:'two',title:'Second page',description:'Also readable'}],cursor:'target',next:null,scan:{at:'today'}});
 assert.equal(await last,true);assert.equal(h.state().data.remoteCursor,'target');assert.equal(h.state().data.items[1].title,'Second page');assert.equal(h.state().data.annotations.one.note,'My note');
});
