const {test}=require('node:test'),assert=require('node:assert/strict'),vm=require('node:vm'),fs=require('node:fs'),path=require('node:path');
const code=fs.readFileSync(path.join(__dirname,'../app/client.js'),'utf8'),R=require('../app/check.js');
function section(from,to){return code.slice(code.indexOf(from),code.indexOf(to));}
function searchHarness(){
 const h=vm.createContext({console,Promise,Error});
 vm.runInContext(`let goal='old goal',choice='',working=false,searchGeneration=0,searchCoverage=null,searchProgress='',ai=true,aiReady=false,answer=null,scope='account:a',log=[],resolveSearch;
 const reads=new Map();const data={items:[],guides:[]};const C={chooseStart:()=>({status:'no_match'}),semanticStart:()=>({status:'ready',source:{id:'old'}})};
 const t=(a,b)=>a,libraryKey=()=>scope,$=()=>null,render=()=>log.push('render');
 const RedBotAI={setScope:s=>log.push(s),progress:()=>{},load:async()=>{log.push('load')},search:()=>new Promise(r=>resolveSearch=r),cancel:()=>log.push('cancel')};
 const window={RedBotAI};
 ${section('  function cancelSearch()', '  function requirementsHTML(')}
 ${section('  async function findStart(', '  function filtered()')}
 globalThis.start=findStart;globalThis.cancel=cancelSearch;globalThis.state=()=>({answer,working,log,searchProgress});globalThis.finish=()=>resolveSearch({ranked:[],coverage:{rows:401,complete:true,indexedChunks:900,cacheHits:1,persistentCache:true}});globalThis.switchScope=()=>{scope='account:b';resetSearchScope();};globalThis.changeGoal=()=>{cancelSearch();goal='new goal';};`,h);return h;
}
test('persisted semantic preference lazily loads model and reports full actual coverage',async()=>{const h=searchHarness();const pending=h.start();await Promise.resolve();h.finish();await pending;assert(h.state().log.includes('load'));assert(h.state().log.includes('account:a'));assert.equal(h.state().answer.status,'ready');});
test('account switch and query edits cancel stale semantic results',async()=>{for(const action of ['switchScope','changeGoal']){const h=searchHarness();const pending=h.start();await Promise.resolve();h[action]();h.finish();await pending;assert.equal(h.state().answer,null);assert.equal(h.state().working,false);assert(h.state().log.includes('cancel'));}});
function rendering(answer){const h=vm.createContext({answer,R,Error,failure:e=>e.message});vm.runInContext(`const lang='zh',t=(a,b)=>a,esc=s=>String(s??'').replaceAll('<','&lt;'),choices={},credentials={};let status=null,videoStartedAt=0;
 ${section('  function requirementsHTML(', '  function rememberConnection(')}
 ${section('  function answerHTML()', '  async function findStart(')}
 ${section('  function timecode(', '  function detail(')}
 globalThis.html=answerHTML();globalThis.video=videoHTML;`,h);return h;}
test('title-only result cannot be kept as verified and missing requirements are visible',()=>{const h=rendering({status:'needs_reading',source:{title:'减脂食谱'},requirements:[{id:'weight-loss',label:'Weight-loss suitability'}],missing:['Weight-loss suitability'],evidence:[]});assert(!h.html.includes('data-action="keep"'));assert(h.html.includes('还缺少证据'));assert(h.html.includes('减肥／减脂'));});
test('full source claims are shown with limits; no-match avoids blaming the goal',()=>{const h=rendering({status:'ready',source:{title:'午餐'},requirements:[{id:'weight-loss',label:'weight'}],evidence:[{text:'这是原文的完整减脂餐声明。'}]});assert(h.html.includes('这是原文的完整减脂餐声明。'));assert(h.html.includes('不是 RedBot 对营养'));const n=rendering({status:'no_match',requirements:[],missing:[]});assert(!n.html.includes('换个更具体'));});
test('raw video details retain timestamped evidence and remain collapsed with source limits',()=>{const h=rendering(null);const html=h.video({type:'video',id:'a'.repeat(24),videoAnalysis:{complete:false,coverage:{audio:'transcribed',frames:'sampled_ocr'},transcript:[{start:12,end:15,text:'原文语音'}],frames:[{at:20,text:[{text:'画面原文'}]}]}});assert(!/<details\s+open(?:[ >])/.test(html));assert(html.includes('<summary>原始语音转录</summary>'));assert(html.includes('0:12–0:15'));assert(html.includes('原文语音'));assert(html.includes('画面原文'));assert(html.includes('不是完整视觉理解'));assert(html.includes('不能视为读完视频'));assert(html.includes('长视频会分段处理'));assert(!html.includes('100 MB'));});
test('raw source blocks preserve video evidence while idea and default prompt avoid timestamp dumps',()=>{
 const x={title:'test',type:'video',videoAnalysis:{complete:false,transcript:[{start:1,end:2,text:'Speech source'}],frames:[{at:5,text:[{text:'OCR source'}]}],coverage:{visual:'not_performed'},sampling:{allFrames:false}}};
 const blocks=R.blocks(x);assert(blocks.some(b=>b.label==='Video transcript (timestamped)'&&b.text==='[1–2s] Speech source'));assert(blocks.some(b=>b.label.includes('OCR')&&b.text==='[5s] OCR source'));
 const idea=R.idea(x),prompt=R.createPrompt(x);assert.equal(R.shortTake(x).sourceKind,'ocr');assert(idea.includes('OCR source'));assert(prompt.includes('OCR source'));
 for(const text of [idea,prompt]){assert(!/\[\d+(?:[–-]\d+)?s\]/.test(text));assert(!text.includes('visual_understanding'));}
 assert(prompt.includes('sampled OCR may be wrong'));assert(prompt.includes('UNTRUSTED DATA'));
});
test('video completion refresh keeps in-progress note, category, collection and scroll',async()=>{
 const h=vm.createContext({Date,Error});vm.runInContext(`let credentials={},configValidated=true,requestActive=false,status=null,offline=false,onboarding=false,initial=false,lastFetch='',lastJob='',detailId='video',tab='home',auto=false;let readEpoch=0,statusSnapshot={epoch:0,startedAt:0};const reads=new Map([['video',{state:'running',jobId:'v',epoch:0,acceptedAt:0}]]);const item=()=>({type:'video',description:'Fresh video text'}),selected=()=>true,readable=()=>true;const data={items:[{}]};const nodes={'#dialog':{open:true,dataset:{kind:'detail'},scrollTop:77},'#personal-note':{value:'unsaved draft'},'#save-topic':{value:'Design'},'#save-collection':{value:'weekend'},'#account':{}};
 const details=[{open:true,text:'我的笔记与整理'},{open:false,text:'查看原文与读取范围'}].map(d=>({...d,querySelector:s=>({textContent:d.text})}));const $=s=>nodes[s]||null,document={hidden:false,activeElement:{id:'personal-note'},querySelectorAll:s=>s==='#dialog-body details'?details:[]};nodes['#personal-note'].focus=()=>{};
 const t=(a,b)=>a,notify=()=>{},activity=()=>'',updateProgress=()=>{},failure=e=>e.message;async function api(){return {state:'connected',revision:2,job:{id:'v',targetId:'video',kind:'video',state:'done'}};}async function loadLibrary(){}function detail(){details.forEach(d=>d.open=false);nodes['#personal-note'].value='';nodes['#save-topic'].value='';nodes['#save-collection'].value='';nodes['#dialog'].scrollTop=0;}
 ${section('  function refreshDetail()', '  function readProgress(')}
 ${section('  async function reconcileRead(', '  function renderVersion(')}
 ${section('  async function refreshStatus()', '  async function sync()')}
 globalThis.refresh=refreshStatus;globalThis.nodes=nodes;globalThis.details=details;`,h);await h.refresh();assert.equal(h.nodes['#personal-note'].value,'unsaved draft');assert.equal(h.nodes['#save-topic'].value,'Design');assert.equal(h.nodes['#save-collection'].value,'weekend');assert.equal(h.nodes['#dialog'].scrollTop,77);assert.equal(h.details[0].open,true);assert.equal(h.details[1].open,false);
});
test('disconnect preserves offline copy and explicitly reports failed vector-cache deletion',async()=>{
 const h=vm.createContext({Date,Error,JSON,setTimeout:()=>0,Promise});
 vm.runInContext(`let credentials={sessionId:'old'},offlineKey=null,status={},data={items:[{id:'saved'}]},notices=[],stored=[];const target={dataset:{},disabled:false};
 const t=(a,b)=>a,item=()=>null,annotation=()=>({}),libraryKey=()=> 'account:old',cancelSearch=()=>{},api=async()=>{},save=async()=>{},dismiss=()=>{},render=()=>{},notify=m=>notices.push(m),failure=e=>e.message;
 const localStorage={setItem:(k,v)=>stored.push([k,v])},RedBotAI={clearCache:async scope=>({cleared:false})};function rememberConnection(v){credentials=v;}
 async function database(){return {transaction(){const tx={objectStore:()=>({put:(d,key)=>stored.push([key,d])})};Promise.resolve().then(()=>tx.oncomplete());return tx;}};} 
 ${section('  async function act(', '  async function init()')}
 globalThis.run=()=>act('confirm-disconnect',target);globalThis.state=()=>({credentials,offlineKey,data,notices,stored});`,h);
 await h.run();const state=h.state();assert.equal(state.credentials,null);assert.equal(state.offlineKey,'offline:old');assert.equal(state.data.items[0].id,'saved');assert(state.notices.some(s=>s.includes('旧向量缓存未确认删除')));
});
test('normal keyword search includes timestamped video source text',()=>{const C=require('../app/core.js');const x=C.normalize({id:'v',title:'Video',type:'video',videoAnalysis:{transcript:[{start:0,end:2,text:'咖啡研磨与冲煮'}]}});assert(C.score(x,{},'咖啡')>0);});

test("failed video refresh retains prior evidence with an explicit warning",()=>{const C=require("../app/core.js");const v=C.normalizeVideoAnalysis({complete:true,transcript:[{start:0,end:1,text:"prior speech"}],frames:[{at:0,text:[{text:"prior frame",confidence:.92}]}],lastRefreshError:{code:"video_tool_failed",at:"2026-11-04T11:00:00Z",retainedPrevious:true}});assert.equal(v.frames[0].text[0].confidence,.92);assert.equal(v.lastRefreshError.code,"video_tool_failed");const h=rendering(null);const html=h.video({type:"video",videoAnalysis:v});assert(html.includes("上次成功结果"));assert(html.includes("prior speech"));});

test("first video failure does not claim a previous successful read",()=>{const C=require("../app/core.js");const v=C.normalizeVideoAnalysis({complete:false,error:"video_tool_failed",lastRefreshError:{code:"video_tool_failed",retainedPrevious:false}});assert.equal(v.lastRefreshError.retainedPrevious,false);const html=rendering(null).video({type:"video",videoAnalysis:v});assert.equal((html.match(/class="warning"/g)||[]).length,1);assert(html.includes("video_tool_failed"));});
