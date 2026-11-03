const {test}=require('node:test');const assert=require('node:assert/strict');const fs=require('node:fs');const C=require('./app/core.js');
const guides=JSON.parse(fs.readFileSync('./evidence/promotion-guides.json'));
const items=[...new Set(guides.flatMap(g=>g.sourceIds))].map(id=>C.normalize({id,title:id,url:'https://example.com/'+id,research:{points:[['Start','Evidence'],['Then','Observe']]}}));
test('promotion goal asks one outcome question; Google and AI stay distinct',()=>{
 const r=C.chooseStart(items,guides,{},'想宣传我的产品');assert.equal(r.status,'clarify');assert.equal(r.options.length,4);
 for(const [goal,id] of [['让Google搜得到','shared-search'],['希望AI回答提到我','promotion-geo'],['做30秒产品介绍视频','video-shotcraft'],['修改现有宣传片','video-source'],['hypit editable video','video-editable'],['确定产品定位和内容角度','promotion-positioning']]){const x=C.chooseStart(items,guides,{},goal);assert.equal(x.status,'ready',goal);assert.equal(x.guide.id,id,goal);}
});
test('mixed search goals clarify; unsupported request and rejected route recover',()=>{
 assert.equal(C.chooseStart(items,guides,{},'SEO and GEO').status,'clarify');
 assert.equal(C.chooseStart(items,guides,{},'quantum telescope').status,'no_match');
 const goal='做30秒产品介绍视频';assert.equal(C.chooseStart(items,guides,{goalState:{skips:{[C.hash(goal)]:['video-shotcraft']}}},goal).status,'no_match');
});
test('instructions retain source identity, real inputs, paid-action boundary and provenance',()=>{
 for(const g of guides){const n=C.normalizeGuide(g);assert.match(n.prompt,/Audience and current problem/);assert.match(n.prompt,/Do not publish/);assert.ok(n.provenance);assert.ok(n.sourceIds.length);assert.match(n.prompt,/Output:/);}
});
