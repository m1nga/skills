const {test} = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../app/client.js'), 'utf8');
function harness(fetch, hostname = 'redbot.example') {
  const saved = {api:'https://old.example',token:'private',sessionId:'existing'};
  const context = vm.createContext({fetch, URL, AbortSignal, location:{hostname,origin:`https://${hostname}`,href:`https://${hostname}/redbot/`}, saved});
  vm.runInContext(`let credentials = saved, config = {}, bootstrapPending, configValidated = false, connectionError = 'old error';
    function rememberConnection(value) {credentials=value;}
    ${source.slice(source.indexOf('  async function refreshConnectionConfig()'), source.indexOf('  function showConnectionError'))}
    globalThis.refresh = refreshConnectionConfig;
    globalThis.state = () => ({credentials,config,connectionError,configValidated});`, context);
  return context;
}
const ok = api => ({ok:true,json:async()=>({api})});
test('failed initial load can recover on explicit retry and updates endpoint while preserving identity', async()=>{
  let count=0;
  const h=harness(async(url,options)=>{
    assert.equal(String(url),'https://redbot.example/redbot/connection.json');
    assert.equal(options.credentials,'omit');
    assert.equal(options.redirect,'error');
    assert.equal(options.cache,'no-store');
    assert.ok(options.signal);
    assert.equal(options.headers,undefined);
    if(!count++) throw Error('offline');
    return ok('https://new.example');
  });
  await assert.rejects(h.refresh(), /connection_config_unavailable/);
  assert.equal(h.state().configValidated,false);
  assert.equal(h.state().credentials.api,'https://old.example');
  assert.equal(h.state().credentials.token,'private');
  await h.refresh();
  assert.equal(h.state().credentials.api,'https://new.example');
  assert.equal(h.state().credentials.sessionId,'existing');
  assert.equal(h.state().connectionError,'');
  assert.equal(h.state().configValidated,true);
});
test('rejects malformed, unsafe or non-OK config without erasing saved credentials',async()=>{
  for(const response of [ok('https://evil.example/path'),ok('http://evil.example'),ok('https://user@evil.example'),ok(''),{ok:false}, {ok:true,json:async()=>{throw Error('invalid JSON');}}]) {
    const h=harness(async()=>response);
    await assert.rejects(h.refresh(),/connection_config_unavailable/);
    assert.equal(h.state().credentials.api,'https://old.example');
    assert.equal(h.state().credentials.token,'private');
  }
});
test('concurrent refresh shares one read; later retry reads config again',async()=>{
  let reads=0;
  const h=harness(async()=>{reads++;return ok('https://new.example');});
  await Promise.all([h.refresh(),h.refresh()]);
  assert.equal(reads,1);
  await h.refresh();
  assert.equal(reads,2);
});
test('local preview uses only verified local capabilities',async()=>{
  const h=harness(async(url,options)=>{
    assert.equal(url,'/api/capabilities');
    assert.equal(options.credentials,'omit');
    assert.ok(options.signal);
    return {ok:true,json:async()=>({redbotConnector:1})};
  },'localhost');
  await h.refresh();
  assert.equal(h.state().credentials.api,'https://localhost');
});

test('signup connect reuses freshly validated config and failure switches to existing-session retry',async()=>{
  const context=vm.createContext({Error,Date});
  vm.runInContext(`let reads=0, dialogs=0, shown='', status={state:'needs_sign_in'}, startedAt=0, onboarding=false;
    async function refreshConnectionConfig(){reads++;}
    async function api(){throw Error('service_offline');}
    function connectionDialog(){dialogs++;}
    function showConnectionError(error){shown=error.message;}
    async function refreshStatus(){}
    ${source.slice(source.indexOf('  async function startLogin('), source.indexOf('  async function refreshStatus()'))}
    globalThis.start=startLogin;
    globalThis.state=()=>({reads,dialogs,shown});`,context);
  await context.start({configReady:true});
  assert.equal(context.state().reads,0);
  assert.equal(context.state().dialogs,1);
  assert.equal(context.state().shown,'service_offline');
  await context.start();
  assert.equal(context.state().reads,1);
});
test('an unvalidated saved endpoint cannot receive a bearer request',async()=>{
  const context=vm.createContext({Error});
  vm.runInContext(`let configValidated=false, sent=0, credentials={token:'private'};
    function apiURL(){return 'https://stale.example';}
    async function fetch(){sent++;}
    ${source.slice(source.indexOf('  async function api(path, body)'), source.indexOf('  function failure(error)'))}
    globalThis.request=api;
    globalThis.count=()=>sent;`,context);
  await assert.rejects(context.request('/api/connection'),/connection_config_unavailable/);
  assert.equal(context.count(),0);
});

test('expired session becomes the same saved offline library without deletion or replay',async()=>{
  const context=vm.createContext({Error,JSON});
  vm.runInContext(`let credentials={sessionId:'old',token:'private'}, offlineKey=null, status={}, onboarding=true, offline=true, connectionError='', calls=[];
    const localStorage={setItem:(key,value)=>calls.push(['store',key,value])};
    async function save(){calls.push(['save',credentials.sessionId]);}
    function rememberConnection(value){credentials=value;calls.push(['forget']);}
    function failure(){return 'Session expired';}
    function render(){calls.push(['render']);}
    function connectionDialog(){calls.push(['dialog']);}
    ${source.slice(source.indexOf('  async function recoverExpiredConnection('),source.indexOf('  async function api(path, body)'))}
    globalThis.recover=recoverExpiredConnection;
    globalThis.state=()=>({credentials,offlineKey,status,connectionError,calls});`,context);
  await context.recover('old');
  const state=context.state();
  assert.equal(state.credentials,null);
  assert.equal(state.offlineKey,'account:old');
  assert.equal(state.status,null);
  assert.equal(state.connectionError,'Session expired');
  assert.equal(state.calls[0][0],'save');
  assert.equal(state.calls[0][1],'old');
  assert.equal(state.calls[1][2],JSON.stringify('account:old'));
  assert.equal(state.calls[2][0],'forget');
  assert.equal(state.calls[4][0],'dialog');
  await context.recover('old');
  assert.equal(context.state().calls.length,5);
});
test('only authenticated 401 session_expired triggers recovery, without replaying request',async()=>{
  for(const [status,error,recoveries] of [[401,'session_expired',1],[503,'session_expired',0],[401,'invite_required',0]]){
    const context=vm.createContext({Error,AbortSignal,status,error});
    vm.runInContext(`let configValidated=true, credentials={sessionId:'old',token:'private'}, requests=0, recovered=[];
      function apiURL(){return 'https://trusted.example';}
      async function fetch(){requests++;return {ok:false,status,json:async()=>({error})};}
      async function recoverExpiredConnection(id){recovered.push(id);}
      ${source.slice(source.indexOf('  async function api(path, body)'),source.indexOf('  function failure(error)'))}
      globalThis.request=api;globalThis.state=()=>({requests,recovered});`,context);
    await assert.rejects(context.request('/api/connect',{}),new RegExp(error));
    assert.equal(context.state().requests,1);
    assert.equal(context.state().recovered.length,recoveries);
    if(recoveries)assert.equal(context.state().recovered[0],'old');
  }
});
