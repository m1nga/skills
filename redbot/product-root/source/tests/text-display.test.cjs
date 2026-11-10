const {test}=require('node:test'),assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const T=require('../app/text.js');
test('pinned local converter simplifies prose without changing code or links',()=>{
  assert.equal(T.simplify('請檢查設定，保留資料。'),'请检查设定，保留资料。');
  const protectedText='`繁體代碼` https://example.test/繁體\n```js\nconst text="繁體";\n```';
  assert.equal(T.simplify(protectedText),protectedText);
});
test('local dictionary and license files match the committed pin',()=>{
  const dir=path.join(__dirname,'../app/vendor/opencc'),lock=JSON.parse(fs.readFileSync(path.join(dir,'assets.lock.json')));
  for(const [name,expected] of Object.entries(lock.files)){
    const bytes=fs.readFileSync(path.join(dir,name));assert.equal(bytes.length,expected.bytes);
    assert.equal(crypto.createHash('sha256').update(bytes).digest('hex'),expected.sha256);
  }
  assert.equal(lock.version,'1.4.2');assert(lock.license.includes('Apache-2.0'));
});
