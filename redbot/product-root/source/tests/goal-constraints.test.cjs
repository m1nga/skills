const {test}=require('node:test'),assert=require('node:assert/strict'),C=require('../app/core.js');
const goal='我想自己做饭，有什么适合减肥吃的';
const dessert={id:'dessert',title:'🇭🇰最好吃的焦糖布蕾',description:'香港餐厅探店，甜品推荐'};
const lunch={id:'lunch',title:'减脂午餐',description:'减脂午餐食谱：食材与制作步骤。'};
test('Chinese goal terms omit filler and bridge weight-loss synonyms',()=>{const terms=C.goalTerms(goal);assert(!terms.includes('吃的'));assert(terms.includes('减脂'));assert.equal(C.chooseStart([dessert,lunch],[],{},goal).source.id,'lunch');});
test('irrelevant body and unread title cannot certify suitability',()=>{assert.equal(C.chooseStart([dessert],[],{},goal).status,'no_match');const r=C.chooseStart([{id:'x',title:'减脂食谱'}],[],{},goal);assert.equal(r.status,'needs_reading');assert(r.missing.includes('Weight-loss suitability'));});
test('semantic score cannot override requirements',()=>{assert.equal(C.semanticStart([dessert],[],{},goal,[{kind:'save',id:'dessert',score:.99}]).status,'no_match');const r=C.semanticStart([dessert,lunch],[],{},goal,[{kind:'save',id:'dessert',score:.99},{kind:'save',id:'lunch',score:.7}]);assert.equal(r.source.id,'lunch');assert(r.evidence.length===2);});
test('explicit cost, equipment and exclusion constraints need evidence',()=>{assert.equal(C.goalEvidence('免费工具',{description:'必须付费的工具'}).status,'conflict');assert.equal(C.goalEvidence('无器械训练',{description:'需要哑铃的训练'}).status,'conflict');assert.equal(C.goalEvidence('不要花生',{description:'花生食谱'}).status,'conflict');assert.equal(C.goalEvidence('不含花生',{description:'不含花生的食谱'}).status,'supported');assert.equal(C.goalEvidence('便宜食谱',{description:'食谱步骤'}).status,'insufficient');});
test('negated and marketing weight-loss mentions do not establish suitability',()=>{
 for(const description of ['不减肥的普通甜点食谱。','并不适合减脂的食谱。','这不是减脂餐，只是普通甜点食谱。','营销案例：用减脂口号推广普通甜品食谱。'])assert.notEqual(C.goalEvidence(goal,{title:'减脂食谱',description}).status,'supported',description);
 assert.equal(C.goalEvidence(goal,{title:'减脂食谱',description:'普通甜点的制作步骤。'}).status,'insufficient');
 assert.equal(C.goalRequirements('我不减肥，只想做饭').some(r=>r.id==='weight-loss'),false);
 assert.equal(C.goalEvidence('我不减肥，只想做饭',lunch).status,'conflict');
});
test('free claims reject negation and post-trial charges; no-money is not a noun exclusion',()=>{
 for(const description of ['并非免费的工具。','免费试用，试用后收费。','免费体验三天后需订阅。'])assert.equal(C.goalEvidence('免费工具',{description}).status,'conflict');
 assert.deepEqual(C.goalRequirements('不要钱的工具').map(r=>r.id),['free']);
});
test('semantic unknown titles must support every parsed requirement',()=>{
 const r=C.semanticStart([{id:'dessert',title:'最好吃的焦糖布蕾'},lunch],[],{},goal,[{id:'dessert',kind:'save',score:.99},{id:'lunch',kind:'save',score:.7}]);assert.equal(r.source.id,'lunch');
 assert.equal(C.semanticStart([{id:'x',title:'减脂午餐'}],[],{},goal,[{id:'x',kind:'save',score:.99}]).status,'no_match');
});
test('evidence is a full source assertion, not a nutrition verdict',()=>{
 const r=C.goalEvidence(goal,lunch);assert.equal(r.evidence.find(e=>e.requirement==='weight-loss').text,lunch.description);assert(r.evidence.every(e=>e.basis==='source_claim'));
 assert.equal(C.chooseStart([lunch],[],{},'减脂食谱，必须适合肾病患者').status,'no_match');
});
test('video analysis whitelist retains transcript/OCR and rejects private URLs',()=>{
 const n=C.normalize({id:'v',title:'Video',videoURL:'https://example.com/v.mp4?signature=secret',videoAnalysis:{pipeline:'local',durationSeconds:12,localCompute:true,cloudCalls:0,visualUnderstanding:false,transcript:[{start:0,end:2,text:'减脂午餐食谱。',url:'https://secret'}],frames:[{at:1,text:[{text:'制作步骤。',confidence:'0.9'}],path:'/private/frame.png'}],coverage:{audio:'transcribed',frames:'sampled_ocr',visual:'not_performed'},sampling:{method:'uniform',intervalSeconds:2},complete:true,sourceVersion:'a'.repeat(64),cached:false,readAt:'2026-11-04T00:00:00Z',signedURL:'https://private',cookie:'secret'}});
 assert.equal(n.videoURL,'');assert.equal(n.videoAnalysis.transcript[0].text,'减脂午餐食谱。');assert(!JSON.stringify(n.videoAnalysis).includes('secret'));assert(!JSON.stringify(n.videoAnalysis).includes('/private'));assert.equal(C.goalEvidence(goal,n).status,'supported');
});
