// Offline wire-shape fixtures, not evidence of a live Xiaohongshu account scan.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const source = fs.readFileSync(process.argv[2] || path.join(__dirname, '../.build/xhs-source/xiaohongshu/redbot_scan.go'), 'utf8');
const js = source.match(/const redbotObservePagination = `([\s\S]*?)`/)[1];
const A = 'a'.repeat(24), B = 'b'.repeat(24);
const endpoint = 'https://edith.xiaohongshu.com/api/sns/web/v2/note/collect/page';
function make(requestPath=endpoint) {
  let answer;
  class XHR { open() {} send() {} addEventListener(_type, fn) { this.loaded = fn; } }
  const context = { URL, Set, XMLHttpRequest: XHR, location:{href:'https://www.xiaohongshu.com/explore'} };
  context.window = context;
  context.fetch = async () => answer;
  vm.runInNewContext(js, context);
  return {context, send:async (cursor, data, extra={}) => {
    const url = requestPath + '?cursor=' + cursor;
    answer = {url, clone:() => ({json:async () => ({success:true, data, ...extra})})};
    await context.fetch(url); await new Promise(resolve => setImmediate(resolve));
    return context.__REDBOT_PAGINATION__;
  }};
}
(async () => {
  const {send,context} = make();
  let state = await send('', {has_more:true, cursor:'next', notes:[{note_id:A}]});
  assert.equal(state.startedAtBeginning, true);
  assert.equal(state.hasMore, true);
  state = await send('next', {has_more:false, cursor:'end', notes:[{note_id:B}]});
  assert.equal(state.chainValid, true);
  assert.equal(state.hasMore, false);
  assert.deepEqual(Array.from(state.seenIds), [A,B]);
  assert.equal(JSON.stringify(state.responses).includes(A), false, 'diagnostics must not contain note IDs');
  assert.equal(JSON.stringify(state.responses).includes('cursor=next'), false, 'diagnostics must not contain cursor URLs');
  assert.equal((await make(endpoint.replace('/note/', '/user/')).send('', {has_more:false,notes:[{id:A}]})).chainValid, true);

  const gap = make();
  await gap.send('', {has_more:true, cursor:'next', notes:[{id:A}]});
  assert.equal((await gap.send('skipped', {has_more:false, notes:[{id:B}]})).chainValid, false);
  assert.equal((await make().send('orphan', {has_more:false, notes:[{id:B}]})).startedAtBeginning, false);
  assert.equal((await make().send('', {has_more:'false', notes:[]})).observed, false);
  assert.equal((await make().send('', {has_more:false, notes:[]}, {success:false})).sourceError, true);
  assert.equal((await make().send('', {has_more:true, notes:[]})).chainValid, false);
  const incomplete = make();
  await incomplete.send('', {has_more:true, cursor:'next', notes:[{note_id:A}]});
  let missing = await incomplete.send('next', {});
  assert.equal(missing.incompleteResponses, 1, 'success with empty data must stop as an incomplete source response');
  assert.equal(missing.hasMore, true, 'last valid page still promised more; empty data is not a last page');
  assert.equal(missing.responses.at(-1).dataType, 'object');
  assert.equal((await incomplete.send('next', {has_more:false, notes:[{note_id:B}]})).incompleteResponses, 0);

  // XHR uses the same observer; no real network or credentials are involved.
  const xhr = new context.XMLHttpRequest();
  xhr.open('GET', endpoint + '?cursor='); xhr.send();
  xhr.responseText = JSON.stringify({success:true,data:{has_more:false,notes:[]}});
  xhr.loaded();
  assert.equal(context.__REDBOT_PAGINATION__.hasMore, false);
  assert.equal(context.__REDBOT_PAGINATION__.chainValid, true);
  assert.equal(context.__REDBOT_PAGINATION__.seenIds.length, 0);

  const large = Array.from({length:2507}, (_,i) => ({id:i.toString(16).padStart(24,'0')}));
  assert.equal((await make().send('', {has_more:false, notes:large})).seenIds.length, 2507);
  console.log('Pagination observer fixtures passed: fetch/XHR, cursor continuity, >2000, errors and schema drift.');
})().catch(error => { console.error(error); process.exitCode = 1; });
