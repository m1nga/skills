// Deterministic algorithm tests only: fixture vectors do NOT validate model quality.
const {test}=require('node:test'),assert=require('node:assert/strict');
const engine=import('../app/semantic-engine.mjs');
function fixture(){let calls=0;const fn=async texts=>{calls+=texts.length;return {tolist:()=>texts.map(t=>t.includes('TARGET')?[1,0]:[0,1])};};fn.tokenizer={encode:t=>Array.from(t).map(c=>c.codePointAt(0)),decode:a=>String.fromCodePoint(...a)};fn.calls=()=>calls;return fn;}
function cache(){const records=new Map();return {persistent:true,records,get:async k=>records.get(k),put:async(k,scope,vector)=>records.set(k,{scope,vector}),prune:async(scope,keep)=>{for(const [k,v]of records)if(v.scope===scope&&(!keep||!keep.has(k)))records.delete(k);}};}
test('full library includes row 351 and long-text tail; resume uses cache and scope isolates',async()=>{
 const {retrieve}=await engine,extractor=fixture(),store=cache();
 const rows=Array.from({length:351},(_,i)=>({id:String(i),kind:'save',text:`save ${i} ordinary`}));rows[350].text='x'.repeat(3500)+'TARGET';
 const run=scope=>retrieve({rows,query:'TARGET',scope,extractor,cache:store});
 const first=await run('account-A');assert.equal(first.ranked[0].id,'350');assert.equal(first.coverage.rows,351);assert.ok(first.ranked[0].bestChunk>30);assert.equal(first.coverage.complete,true);
 const second=await run('account-A');assert.equal(second.coverage.cacheHits,second.coverage.totalChunks);
 const third=await run('account-B');assert.equal(third.coverage.cacheHits,first.coverage.cacheHits); // Within-run repeated chunks may hit; account A must add no hits.
 assert.ok([...store.records.values()].some(v=>v.scope!==[...store.records.values()][0].scope));
});
test('cancellation retains completed batches and resume can finish',async()=>{
 const {retrieve}=await engine,extractor=fixture(),store=cache();let stop=false;
 const input={rows:[{id:'long',text:'x'.repeat(900)+'TARGET'}],query:'TARGET',scope:'A',extractor,cache:store};
 await assert.rejects(retrieve({...input,cancelled:()=>stop,progress:()=>{stop=true;}}),/cancelled/);assert.ok(store.records.size);
 const done=await retrieve(input);assert.ok(done.coverage.cacheHits);assert.equal(done.coverage.complete,true);
});
test('cache open failure degrades safely to local inference without persistence',async()=>{
 const {VectorCache,retrieve}=await engine;const store=await new VectorCache({open(){throw Error('denied');}}).open();assert.equal(store.persistent,false);
 const result=await retrieve({rows:[{id:'one',text:'TARGET'}],query:'TARGET',scope:'A',extractor:fixture(),cache:store});assert.equal(result.ranked[0].id,'one');assert.equal(result.coverage.persistentCache,false);
});
test('bounded token windows cover tail with overlap',async()=>{
 const {chunks}=await engine;const text='0123456789'.repeat(40)+'TAIL';const out=chunks(text,fixture().tokenizer);assert.ok(out.every(s=>s.length<=100));assert.ok(out.at(-1).endsWith('TAIL'));assert.equal(out[0].slice(-20),out[1].slice(0,20));
});
test('vendored runtime files match pinned provenance lock',()=>{
 const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');const root=path.join(__dirname,'../app/vendor/transformers');const lock=JSON.parse(fs.readFileSync(path.join(root,'assets.lock.json')));
 for(const [name,entry]of Object.entries(lock)){const data=fs.readFileSync(path.join(root,name));assert.equal(data.length,entry.bytes);assert.equal(crypto.createHash('sha256').update(data).digest('hex'),entry.sha256);assert.ok(!entry.url.includes('@latest'));}
});
test('semantic request includes normalized video transcript and sampled OCR without transport metadata',async()=>{
 const fs=require('node:fs'),vm=require('node:vm'),C=require('../app/core.js');const messages=[];
 class Worker{constructor(){this.onmessage=null;}postMessage(message){messages.push(message);queueMicrotask(()=>this.onmessage({data:{id:message.id,ranked:[]}}));}}
 const context={window:{},Worker,document:{baseURI:'https://example.test/'},URL,crypto:require('node:crypto').webcrypto,Error,queueMicrotask,setTimeout,clearTimeout};
 vm.runInNewContext(fs.readFileSync(require('node:path').join(__dirname,'../app/ai.js'),'utf8'),context);
 const item=C.normalize({id:'video',title:'Video example',url:'https://example.test/video',type:'video',videoAnalysis:{transcript:[{start:1,end:2,text:'免费语音转录保留完整的音频尾部'}],frames:[{at:2,text:[{text:'OCR only instruction visible on a sampled frame',confidence:.9}]}],cookie:'DO_NOT_SEND_COOKIE',videoURL:'DO_NOT_SEND_URL'}});
 await context.window.RedBotAI.search('convert speech',[item],[],{});
 const request=messages.find(m=>m.action==='search');assert.ok(request.rows[0].text.includes('免费语音转录保留完整的音频尾部'));assert.ok(request.rows[0].text.includes('OCR only instruction visible on a sampled frame'));assert.ok(!JSON.stringify(request).includes('DO_NOT_SEND'));
});
