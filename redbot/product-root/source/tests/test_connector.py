"""Deterministic isolation/recovery tests. Fake source, not a real-account trial."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import threading
import time
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

spec = importlib.util.spec_from_file_location('connector_service', Path(__file__).parents[1] / 'connector/service.py')
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)
A, B = 'a' * 24, 'b' * 24


def card(nid=A, title='A free tool', token='private-source-token'):
    return {'id': nid, 'xsecToken': token, 'noteCard': {'displayTitle': title, 'type': 'normal', 'user': {'nickname': 'Author'}, 'cover': {}}}


class Fake:
    def __init__(self, binary, directory):
        self.directory, self.uid, self.calls, self.stopped = directory, 'account-A', [], False
        self.profile = {'feeds': [card()]}
        self.logged = True

    def request(self, method, path, body=None):
        self.calls.append((method, path, body))
        if path.endswith('/status'):
            return {'is_logged_in': self.logged, 'user_id': self.uid, 'username': 'Test user'}
        if path.endswith('tab=fav'):
            return {'data': self.profile}
        if path.endswith('/detail'):
            return {'data': {'note': {'desc': 'Original text', 'title': 'A free tool'}}}
        if path.endswith('/qrcode'):
            return {'img':'data:image/png;base64,YQ==', 'is_logged_in': False}
        raise AssertionError(path)

    def cookie_stamp(self):
        return None

    def stop(self):
        self.stopped = True


class ConnectorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = S.Store(Path(self.temp.name), Path('/unused'), capacity=3, factory=Fake)

    def tearDown(self):
        self.store.stop()
        self.temp.cleanup()

    def new(self):
        token = self.store.create(self.store.config['invite'], True)['token']
        return token, self.store.get(token)

    def test_requires_invite_and_consent(self):
        for invite, consent in [('bad', True), (self.store.config['invite'], False)]:
            with self.assertRaises(S.Problem): self.store.create(invite, consent)

    def test_separate_paths_tokens_and_libraries(self):
        ta, a = self.new(); tb, b = self.new()
        self.assertNotEqual(a.directory, b.directory)
        self.assertNotEqual(ta, tb)
        a.verify(); a.scan()
        self.assertEqual(len(a.library['items']), 1)
        self.assertEqual(b.library['items'], [])
        self.assertNotIn('private-source-token', json.dumps(a.library))
        self.assertEqual(a.directory.stat().st_mode & 0o777, 0o700)
        self.assertEqual((a.directory/'source-tokens.json').stat().st_mode & 0o777, 0o600)

    def test_login_required_before_read_or_scan(self):
        _, session = self.new()
        with self.assertRaises(S.Problem): session.scan()
        with self.assertRaises(S.Problem): session.read(A)
        self.assertEqual(session.backend.calls, [])

    def test_different_account_cannot_merge(self):
        _, session = self.new(); session.verify(); session.scan()
        before = json.dumps(session.library)
        session.backend.uid = 'account-B'
        with self.assertRaises(S.Problem): session.scan()
        self.assertEqual(before, json.dumps(session.library))
        self.assertEqual(session.state, 'wrong_account')

    def test_recover_current_scan_checkpoint_only(self):
        _, session = self.new(); session.verify(); session.scan()
        original = session.backend.request
        def interrupted(method, path, body=None):
            if path.endswith('tab=fav'):
                S.atomic(session.directory/'scan-checkpoint.json', {'feeds':[card(B)]})
                raise S.Problem('source_unavailable', 502)
            return original(method, path, body)
        session.backend.request = interrupted
        session.scan()
        self.assertEqual({x['id'] for x in session.library['items']}, {A,B})
        self.assertTrue(session.library['scan']['interrupted'])
        self.assertFalse(session.library['scan']['complete'])
        self.assertEqual(session.library['scan']['kept'], 1)

    def test_stale_checkpoint_does_not_replace_library(self):
        _, session = self.new(); session.verify(); session.scan()
        checkpoint=session.directory/'scan-checkpoint.json'
        S.atomic(checkpoint, {'feeds':[card(B)]})
        os.utime(checkpoint, (time.time()-100, time.time()-100))
        original=session.backend.request
        def failed(method, path, body=None):
            if path.endswith('tab=fav'): raise S.Problem('source_unavailable', 502)
            return original(method, path, body)
        session.backend.request=failed
        with self.assertRaises(S.Problem): session.scan()
        self.assertEqual([x['id'] for x in session.library['items']], [A])

    def test_incremental_duplicate_partial_and_notes(self):
        first, _ = S.merge_scan({}, {'feeds':[card(),card()]})
        first['items'][0]['description'] = 'Keep the text'
        first['items'][0]['readingNotes'] = 'Keep my note'
        second, _ = S.merge_scan(first, {'feeds':[card()]})
        self.assertEqual(len(second['items']),1)
        self.assertEqual(second['scan']['unchanged'],1)
        self.assertEqual(second['scan']['added'],0)
        self.assertEqual(second['items'][0]['readingNotes'],'Keep my note')
        partial, _ = S.merge_scan(second, {'feeds':[card(B)]})
        self.assertEqual(len(partial['items']),2)
        self.assertEqual(partial['scan']['kept'],1)
        self.assertFalse(partial['scan']['complete'])
        self.assertEqual(partial['scan']['llmTokens'],0)

    def test_change_marks_read_content_stale_without_erasing(self):
        first,_=S.merge_scan({}, {'feeds':[card()]})
        first['items'][0]['description']='Earlier text'
        second,_=S.merge_scan(first, {'feeds':[card(title='Paid version')]})
        self.assertEqual(second['scan']['changed'],1)
        self.assertTrue(second['items'][0]['sourceMayHaveChanged'])
        self.assertEqual(second['items'][0]['description'],'Earlier text')

    def test_only_own_known_save_can_be_read(self):
        _, session=self.new();session.verify();session.scan()
        with self.assertRaises(S.Problem):session.read(B)
        session.read(A)
        self.assertEqual(session.library['items'][0]['description'],'Original text')
        self.assertEqual(session.library['scan']['readCount'],1)

    def test_disconnect_revokes_token_and_deletes_credentials(self):
        token, session=self.new();session.verify();session.scan()
        self.store.remove(token)
        self.assertFalse(session.directory.exists())
        self.assertTrue(session.backend.stopped)
        with self.assertRaises(S.Problem):self.store.get(token)

    def test_one_job_at_a_time_and_disconnect_cancels_commit(self):
        _,session=self.new(); event=threading.Event()
        session.start('fake',lambda:event.wait(1))
        with self.assertRaises(S.Problem):session.start('duplicate',lambda:None)
        session.close();event.set()
        time.sleep(.03)
        self.assertFalse(session.directory.exists())

    def test_persistent_session_keeps_its_identity(self):
        token,session=self.new();session.verify();session.scan()
        restored=S.Store(Path(self.temp.name),Path('/unused'),factory=Fake)
        recovered=restored.get(token)
        self.assertEqual(recovered.meta['account'],session.meta['account'])
        self.assertEqual(len(recovered.library['items']),1)
        self.assertEqual(recovered.state,'needs_sign_in')

    def test_expired_sessions_are_reaped(self):
        token,session=self.new();session.meta['expires']=time.time()-1
        self.store.reap()
        self.assertFalse(session.directory.exists())
        with self.assertRaises(S.Problem):self.store.get(token)

    def test_adapter_rejects_mutations_before_starting_process(self):
        mcp=S.MCP(Path('/missing'),Path(self.temp.name)/'new')
        with self.assertRaises(S.Problem):mcp.request('POST','/api/v1/feeds/favorite',{})
        self.assertIsNone(mcp.child)

    def test_http_origin_host_auth_and_no_raw_files(self):
        server=S.ThreadingHTTPServer(('127.0.0.1',0),S.BaseHTTPRequestHandler)
        host='127.0.0.1:'+str(server.server_port)
        server.RequestHandlerClass=S.make_handler(self.store,{'https://sidecourt.space'},host)
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        def request(path,token=None,origin=None,wrong_host=False):
            headers={}
            if token:headers['Authorization']='Bearer '+token
            if origin:headers['Origin']=origin
            if wrong_host:headers['Host']='evil.example'
            try:
                with urlopen(Request('http://'+host+path,headers=headers)) as response:return response.status,response.headers,json.load(response)
            except HTTPError as error:return error.code,error.headers,json.load(error)
        try:
            token,session=self.new();session.verify();session.scan()
            self.assertEqual(request('/api/library')[0],401)
            self.assertEqual(request('/api/library',token,'https://evil.example')[0],403)
            self.assertEqual(request('/api/library',token,wrong_host=True)[0],403)
            code,headers,body=request('/api/library',token,'https://sidecourt.space')
            self.assertEqual(code,200)
            self.assertEqual(headers['Access-Control-Allow-Origin'],'https://sidecourt.space')
            self.assertNotIn('xsecToken',json.dumps(body))
            self.assertEqual(request('/sessions/'+session.meta['id']+'/cookies.json',token)[0],404)
            self.assertEqual(request('/api/v1/feeds/favorite',token)[0],404)
        finally:server.shutdown();server.server_close()


if __name__=='__main__':unittest.main()
