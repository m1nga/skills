const {test}=require('node:test');
const assert=require('node:assert/strict');
const vm=require('node:vm');
const fs=require('node:fs');
const source=fs.readFileSync(require('node:path').join(__dirname,'../app/client.js'),'utf8');
const C=require('../app/core.js'),R=require('../app/check.js');
function harness(type='note'){
 const x={id:'6ae38bae000000002c01428d',type,title:'source',description:'',url:'https://www.xiaohongshu.com/explore/6ae38bae000000002c01428d'};
 const nodes={'#dialog':{open:true,dataset:{kind:'detail'},scrollTop:65},'#personal-note':{value:'unsaved thought',focus(){}},'#save-topic':{value:'Creative'},'#save-collection':{value:'mine'}};
 const h=vm.createContext({R,C,Map,Date,Error,AbortSignal,URL,x,nodes,document:{activeElement:{id:'personal-note'}},console});
 vm.runInContext(`let offline=false, savedOkay=true, reloads=0,detailId=x.id, credentials={sessionId:'one'}, status={state:'connected'}, data={items:[x],annotations:{}}, calls=[], renders=0, briefs=0;
 const reads=new Map(), $=q=>nodes[q], item=id=>data.items.find(i=>i.id===id),t=(zh,en)=>zh,esc=String,annotation=id=>data.annotations[id]||{};
 function detail(){renders++;nodes['#personal-note'].value='would be discarded';} function brief(){briefs++;}
 async function api(path,body){calls.push({path,body});return {jobId:'job-'+calls.length};}
 function failure(e){return e.message;} async function save(){return savedOkay;} const APP_VERSION='1.9.2';let latestVersion='',versionCheckedAt=0;
 ${source.slice(source.indexOf('  function readable('),source.indexOf('  function timecode('))}
 globalThis.reload=reloadUpdatedApp;globalThis.checkVersion=checkVersion;globalThis.setSave=value=>savedOkay=value;globalThis.saved=()=>data.annotations[x.id];globalThis.reloads=()=>reloads;globalThis.location={href:'https://redbot.example/app/',reload(){reloads++;}};globalThis.request=requestRead;globalThis.reconcile=reconcileRead;globalThis.readable=readable;globalThis.progress=()=>readProgress(x);
 globalThis.setStatus=value=>status=value;globalThis.setSelected=value=>detailId=value;globalThis.state=()=>({status,calls,r:reads.get(x.id),renders,briefs});`,h);
 return h;
}
test('one selected note read is deduplicated and preserves unsaved detail fields',async()=>{
 const h=harness();await h.request(h.x.id);await h.request(h.x.id);await h.request(h.x.id,{retry:true});
 assert.equal(h.state().calls.length,1);assert.equal(h.state().calls[0].path,'/api/read');
 assert.equal(h.nodes['#personal-note'].value,'unsaved thought');assert.equal(h.nodes['#dialog'].scrollTop,65);
 assert.equal(h.state().r.state,'running');assert.match(h.progress(),/取消读取/);
});
test('video selection reads video and caption alone cannot unlock brief',async()=>{
 const h=harness('video');h.x.description='caption only';assert.equal(h.readable(h.x),false);
 await h.request(h.x.id);assert.equal(h.state().calls[0].path,'/api/video');
 h.x.videoAnalysis={transcript:[{text:'actual spoken method',start:0,end:1}]};assert.equal(h.readable(h.x),true);
});
test('busy selection waits once and closing it prevents queued work from starting',async()=>{
 const h=harness();h.setStatus({job:{id:'other',targetId:'other',kind:'read',state:'running'}});
 await h.request(h.x.id);assert.equal(h.state().r.state,'queued');assert.equal(h.state().calls.length,0);
 h.setSelected(null);h.setStatus({job:{id:'other',targetId:'other',kind:'read',state:'done'}});await h.reconcile();assert.equal(h.state().calls.length,0);
 h.setSelected(h.x.id);await h.reconcile();assert.equal(h.state().calls.length,1);
});
test('other item terminal result cannot complete selected read; failed result remains until explicit retry',async()=>{
 const h=harness();await h.request(h.x.id,{briefAfter:true});
 h.setStatus({job:{id:'other',targetId:'other',kind:'read',state:'failed',error:'source_unavailable'}});await h.reconcile();assert.equal(h.state().r.state,'running');
 h.setStatus({job:{id:'job-1',targetId:h.x.id,kind:'read',state:'failed',error:'source_unavailable'}});await h.reconcile();
 assert.equal(h.state().r.state,'failed');assert.match(h.progress(),/source_unavailable/);assert.equal(h.state().briefs,0);
 await h.request(h.x.id);assert.equal(h.state().calls.length,1);
 await h.request(h.x.id,{retry:true});assert.equal(h.state().calls.length,2);
});
test('done with empty content does not open an empty brief; actual source completion does',async()=>{
 const h=harness();await h.request(h.x.id,{briefAfter:true});
 h.setStatus({job:{id:'job-1',targetId:h.x.id,kind:'read',state:'done'}});await h.reconcile();assert.equal(h.state().briefs,0);assert.match(h.state().r.error,/没有取得可用内容/);
 await h.request(h.x.id,{retry:true,briefAfter:true});h.x.description='Useful actual method';
 h.setStatus({job:{id:'job-2',targetId:h.x.id,kind:'read',state:'done'}});await h.reconcile();assert.equal(h.state().briefs,1);
});
test('normalization preserves sanitized read outcome needed after page restore',()=>{
 const x=C.normalize({id:'6ae38bae000000002c01428d',description:'retained',contentReadStatus:'failed',contentReadError:{code:'source_unavailable',at:'now',retainedPrevious:true,secret:'never'},contentReadAt:'then'});
 assert.equal(x.contentReadStatus,'failed');assert.equal(x.contentReadError.retainedPrevious,true);assert.equal(x.contentReadError.secret,undefined);assert.equal(x.contentReadAt,'then');
});

test('update reload saves the live note and refuses reload if saving fails',async()=>{
 const h=harness();h.setSave(false);await h.reload();assert.equal(h.reloads(),0);assert.equal(h.saved().note,'unsaved thought');
 h.setSave(true);await h.reload();assert.equal(h.reloads(),1);assert.equal(h.saved().category,'Creative');assert.deepEqual(Array.from(h.saved().collections),['mine']);
});
test('version checks use only same-origin no-store unauthenticated requests and throttle repeats',async()=>{
 const h=harness();let count=0;h.nodes['#app-update']={hidden:true};
 h.fetch=async(url,opts)=>{count++;assert.equal(String(url),'https://redbot.example/app/version.json');assert.equal(opts.cache,'no-store');assert.equal(opts.credentials,'omit');assert.equal(opts.headers,undefined);return {ok:true,json:async()=>({version:'1.9.3'})};};
 await h.checkVersion();await h.checkVersion();assert.equal(count,1);assert.equal(h.nodes['#app-update'].hidden,false);assert.equal(h.reloads(),0);
});
function useRealDetail(h){
 vm.runInContext(`let detailHTML='';data.collections=[];const label=x=>x||'',videoHTML=()=>'',commentsHTML=()=>'',sourceText=x=>x.description||'',repoHTML=()=>'';function modal(html){detailHTML=html;}
 ${source.slice(source.indexOf('  function detail('),source.indexOf('  function repoHTML('))}
 globalThis.openDetail=()=>detail(x.id);globalThis.detailHTML=()=>detailHTML;`,h);
}
test('actual detail auto-reads once and exposes claim/brief tools only after source exists',async()=>{
 const h=harness();useRealDetail(h);h.openDetail();await Promise.resolve();
 assert.equal(h.state().calls.length,1);assert(!h.detailHTML().includes('免费、广告、收费'));assert(!h.detailHTML().includes('整理执行指令'));
 h.openDetail();assert.equal(h.state().calls.length,1);
 h.x.description='Actual useful source body';h.openDetail();assert(h.detailHTML().includes('Actual useful source body'));assert(h.detailHTML().includes('整理执行指令'));
});
test('restored failed source remains actionable without silently retrying on open',async()=>{
 const h=harness();h.x.contentReadStatus='failed';h.x.contentReadError={code:'source_unavailable'};useRealDetail(h);h.openDetail();await Promise.resolve();
 assert.equal(h.state().calls.length,0);assert(h.detailHTML().includes('重试读取'));assert(h.detailHTML().includes('source_unavailable'));
});
