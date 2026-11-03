const {test}=require('node:test'),a=require('node:assert/strict'),C=require('./app/core.js');
test('semantic choice keeps saved evidence, thresholds and personal notes distinct',()=>{
 const items=[C.normalize({id:'read',title:'A note',url:'https://example.com',description:'Change one section at a time.'}),C.normalize({id:'unread',title:'A video',url:'https://example.com/video'})];
 a.equal(C.semanticStart(items,[],{},'indirect words',[{id:'read',kind:'save',score:.7}]).status,'ready');
 a.equal(C.semanticStart(items,[],{},'indirect words',[{id:'unread',kind:'save',score:.8}]).status,'needs_reading');
 a.equal(C.semanticStart(items,[],{},'unrelated',[{id:'read',kind:'save',score:.1}]).status,'no_match');
 a.equal(C.semanticStart(items,[],{annotations:{read:{trashed:true}}},'indirect words',[{id:'read',kind:'save',score:.7}]).status,'no_match');
 a.equal(C.semanticStart(items,[],{annotations:{unread:{note:'My actual observation'}}},'indirect words',[{id:'unread',kind:'save',score:.7}]).status,'ready');
});
