import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const html=readFileSync(new URL('../assets/companion.html',import.meta.url),'utf8');
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
new vm.Script(script);
const ctx=vm.createContext({assert});
vm.runInContext(script.split('let bundle=sample')[0]+`
validate(sample);
assert.equal(eligible(sample,'advance',10).length,1);
assert.equal(total(eligible(sample,'advance',10)[0]),8);
assert.equal(eligible(sample,'resume',10).length,1);
assert.equal(eligible(sample,'learn',10).length,1);
for(const field of ['state','owner','authorized','interruptible','conflict_check']){
 const b=JSON.parse(JSON.stringify(sample));
 b.candidates[0][field]=({state:'held',owner:'agent',authorized:false,interruptible:false,conflict_check:'unknown'})[field];
 assert.equal(eligible(b,'advance',20).length,0,field);
}
for(const status of ['finished','waiting_for_user']){
 const b=JSON.parse(JSON.stringify(sample)); b.current_work.agent_status=status;
 assert.equal(eligible(b,'learn',20).length,0);
}
for(const bad of ['false',null,0]){
 const b=JSON.parse(JSON.stringify(sample));b.candidates[0].authorized=bad;
 assert.throws(()=>validate(b));
}
const malformed=JSON.parse(JSON.stringify(sample));malformed.candidates[0].minutes.work=-1;
assert.throws(()=>validate(malformed));
const tight=JSON.parse(JSON.stringify(sample));tight.candidates[0].minutes.work=7;
assert.equal(eligible(tight,'advance',10).length,0);
`,ctx);
assert(!script.includes('innerHTML'));
console.log('PASS: script syntax, example validation, timing budget, ownership/hold/conflict/authorization filters, agent return states, malformed booleans and negative durations, no innerHTML.');
vm.runInContext(`
for(const work of [0,0.5,-1]){const b=JSON.parse(JSON.stringify(sample));b.candidates[0].minutes.work=work;assert.throws(()=>validate(b));}
const ordered=JSON.parse(JSON.stringify(sample));ordered.candidates=[
 {...ordered.candidates[2],id:'z',project:'elsewhere'},
 {...ordered.candidates[2],id:'b',minutes:{setup:1,work:4,wrap:1}},
 {...ordered.candidates[2],id:'a'},
];assert.equal(eligible(ordered,'learn',20).map(c=>c.id).join(','),'a,b,z');
`,ctx);
const sample=vm.runInContext('JSON.parse(JSON.stringify(sample))',ctx);
for(const broken of [
 {version:1,bundle:sample,isExample:true,history:[],session:null,drafts:[{kind:'incomplete',draft:{got:42}}]},
 {version:1,bundle:sample,isExample:true,history:[null],session:null},
 {version:1,bundle:sample,isExample:true,history:[],session:{id:'acceptance',budget:10,elapsed:0,running:false,stage:'checkpoint',draft:{got:42,next:'x',learned:''}}},
 {version:1,bundle:sample,isExample:true,history:[],session:{id:'acceptance',budget:10,elapsed:0,running:false,stage:'returned',checkpoint:{}}},
]){
 const original=JSON.stringify(broken);let saved=original;
 const elements=new Map();
 const document={getElementById(id){if(!elements.has(id))elements.set(id,{hidden:false,textContent:'',value:'',addEventListener(){}});return elements.get(id)},addEventListener(){}};
 const browser=vm.createContext({document,localStorage:{getItem(){return saved},setItem(k,v){saved=v}},setInterval(){},performance:{now(){return 0}},setTimeout(){}});
 vm.runInContext(script,browser);
 assert.equal(vm.runInContext('corrupt',browser),true);
 vm.runInContext('save()',browser);
 assert.equal(saved,original,'Corrupt nested state must remain recoverable');
 assert.equal(elements.get('storageNotice').hidden,false);
}
console.log('PASS: integer work durations, deterministic selection, nested malformed storage preservation and visible recovery notice.');
{
 let saved=null;const elements=new Map();
 const document={getElementById(id){if(!elements.has(id))elements.set(id,{hidden:false,textContent:'',value:'',focus(){}});return elements.get(id)},addEventListener(){}};
 const browser=vm.createContext({document,localStorage:{getItem(){return saved},setItem(k,v){saved=v}},setInterval(){},performance:{now(){return 0}},setTimeout(){}});
 vm.runInContext(script,browser);
 document.getElementById('budget').value='15';document.getElementById('intent').value='advance';
 elements.get('choose').onclick();elements.get('ready').onclick();
 assert.equal(elements.get('immediateReturn').hidden,false);
 assert.equal(elements.get('immediateReturn').textContent,sample.current_work.return_to);
 assert.equal(elements.get('skipNote').hidden,false);
 elements.get('got').value='Unfinished thought';elements.get('next').value='';
 elements.get('skipNote').onclick();
 assert.equal(elements.get('returned').hidden,false);
 assert.equal(elements.get('export').hidden,true);
 const state=JSON.parse(saved);
 assert.equal(state.session.draft.got,'Unfinished thought');
 assert.equal(state.session.skipped,true);
 assert.equal(state.history.length,0);
 assert.equal(state.session.checkpoint,undefined);
 elements.get('another').onclick();
 const replaced=JSON.parse(saved);
 assert.equal(replaced.session,null);
 assert.equal(replaced.drafts.length,1);
 assert.equal(replaced.drafts[0].kind,'incomplete');
 assert.equal(replaced.drafts[0].draft.got,'Unfinished thought');
 assert.equal(elements.get('feedback').textContent,'');
 assert.equal(vm.runInContext('drafts[0].draft.got',browser),'Unfinished thought');
}
console.log('PASS: Agent ready immediately shows return cue; skip bypasses required note, retains draft, and creates no completed checkpoint.');
