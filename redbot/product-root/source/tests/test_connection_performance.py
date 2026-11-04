"""Slow network, incremental sync and credential-bound verification regressions."""
import json
from pathlib import Path
import tempfile
import threading
import time
import unittest
from urllib.request import Request,urlopen
from test_connector import S, Fake, card, A, B

class PerformanceTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.store=S.Store(Path(self.temp.name),Path('/unused'),factory=Fake)
        self.token=self.store.create(self.store.config['invite'],True)['token']
        self.session=self.store.get(self.token)
        self.session.backend.cookie_stamp=lambda: 1
        self.session.verify();self.session.scan()
    def tearDown(self):
        self.store.stop();self.temp.cleanup()
    def identities(self):
        return sum(path.endswith('/status') for _,path,_ in self.session.backend.calls)
    def test_recent_identity_reused_but_changed_cookie_rechecks_account(self):
        self.assertEqual(self.identities(),1)
        self.session.read(A);self.assertEqual(self.identities(),1)
        self.session.backend.uid='account-B';self.session.backend.cookie_stamp=lambda:2
        count=len(self.session.backend.calls)
        with self.assertRaises(S.Problem) as error:self.session.read(A)
        self.assertEqual(error.exception.code,'wrong_account')
        self.assertEqual(self.identities(),2)
        self.assertFalse(any(path.endswith('/detail') for _,path,_ in self.session.backend.calls[count:]))
    def test_expiry_and_source_failure_force_new_verification(self):
        self.session.verified_at=time.monotonic()-S.VERIFIED_TTL-1
        self.session.read(A);self.assertEqual(self.identities(),2)
        original=self.session.backend.request
        def failed(method,path,body=None):
            if path.endswith('/detail'):raise S.Problem('source_unavailable',502)
            return original(method,path,body)
        self.session.backend.request=failed
        with self.assertRaises(S.Problem):self.session.read(A)
        self.assertEqual(self.session.verified_at,0)
        self.session.backend.request=original;self.session.read(A)
        self.assertEqual(self.identities(),3)
    def test_explicit_verification_and_unconfirmed_cookie_always_check(self):
        self.session.verify();self.assertEqual(self.identities(),2)
        self.session.backend.cookie_stamp=lambda:None
        self.session.verify(reuse=True);self.session.verify(reuse=True)
        self.assertEqual(self.identities(),4)
    def test_delta_only_changed_and_new_rows_and_full_after_restart(self):
        first=self.session.library_snapshot();self.assertEqual(first['mode'],'full')
        first['items'][0]['title']='Client cannot mutate the source'
        self.assertNotEqual(self.session.library['items'][0]['title'],first['items'][0]['title'])
        self.assertEqual(self.session.library_snapshot(first['cursor'])['items'],[])
        self.session.library['items'][0]['lastSeenAt']='later'
        self.assertEqual(self.session.library_snapshot(first['cursor'])['items'],[])
        self.session.library['items'].append({'id':B,'title':'New save'})
        changed=self.session.library_snapshot(first['cursor'])
        self.assertEqual([x['id'] for x in changed['items']],[B])
        self.session.library['items'][0]['description']='Newly read source'
        changed2=self.session.library_snapshot(changed['cursor'])
        self.assertEqual([x['id'] for x in changed2['items']],[A])
        S.atomic(self.session.directory/'library.json',self.session.library)
        restored=S.Session(self.session.directory,self.session.meta,Fake(None,self.session.directory))
        self.assertEqual(restored.verified_at,0)
        self.assertEqual(restored.library_snapshot(changed2['cursor'])['mode'],'full')
    def test_cursor_is_account_scoped_and_history_is_bounded(self):
        cursor=self.session.library_snapshot()['cursor']
        other=self.store.get(self.store.create(self.store.config['invite'],True)['token'])
        other.library['items']=[{'id':B,'title':'Other account'}]
        response=other.library_snapshot(cursor)
        self.assertEqual(response['mode'],'full');self.assertEqual([x['id'] for x in response['items']],[B])
        for n in range(20):
            self.session.library['items'][0]['description']=str(n);self.session.library_snapshot()
        self.assertEqual(len(self.session.library_views),16)
        self.assertEqual(self.session.library_snapshot(cursor)['mode'],'full')
    def test_slow_library_delivery_does_not_block_account_status(self):
        entered,release,done=threading.Event(),threading.Event(),threading.Event()
        server=S.ThreadingHTTPServer(('127.0.0.1',0),S.BaseHTTPRequestHandler)
        host='127.0.0.1:'+str(server.server_port);base=S.make_handler(self.store,{'https://sidecourt.space'},host)
        class SlowReceiver(base):
            def send(self,data,*args,**kwargs):
                if isinstance(data,dict) and isinstance(data.get('items'),list):entered.set();release.wait(3)
                return super().send(data,*args,**kwargs)
        server.RequestHandlerClass=SlowReceiver
        threading.Thread(target=server.serve_forever,daemon=True).start()
        def read():
            with urlopen(Request('http://'+host+'/api/library',headers={'Authorization':'Bearer '+self.token}),timeout=5) as r:r.read()
        reader=threading.Thread(target=read);reader.start()
        try:
            self.assertTrue(entered.wait(1))
            def status():self.session.status();done.set()
            checker=threading.Thread(target=status);checker.start()
            self.assertTrue(done.wait(1),'A slow download locked this account')
        finally:
            release.set();reader.join();server.shutdown();server.server_close()

    def test_paged_library_delivers_every_row_and_catches_changes_during_transfer(self):
        rows=[{'id':f'{i:024x}','url':f'https://www.xiaohongshu.com/explore/{i:024x}','description':'text '*12000} for i in range(23)]
        self.session.library['items']=rows
        first=self.session.library_page();self.assertTrue(first['next']);self.assertLess(len(first['items']),len(rows))
        target=first['cursor'];received=list(first['items']);seen_pages=[];next_page=first['next']
        rows[0]['description']='Changed after first page'
        # More than sixteen content revisions during a long paged transfer must
        # not evict its protected starting cursor and cause an endless full loop.
        for i in range(20):rows[1]['title']=str(i);self.session.library_snapshot()
        while next_page:
            result=self.session.library_page(page=next_page);seen_pages.append(next_page)
            self.assertEqual(result['cursor'],target);received+=result['items'];next_page=result['next']
        self.assertEqual([x['id'] for x in received],[x['id'] for x in rows])
        delta=self.session.library_page(cursor=target)
        self.assertEqual(delta['mode'],'delta');self.assertEqual({x['id'] for x in delta['items']},{rows[0]['id'],rows[1]['id']})
        self.assertLessEqual(len(self.session.library_pages),4)
        other=self.store.get(self.store.create(self.store.config['invite'],True)['token'])
        self.assertEqual(other.library_page(page=seen_pages[-1])['items'],[])
        self.assertEqual(self.session.library_page(page='expired-page')['mode'],'full')
