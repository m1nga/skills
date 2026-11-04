"""Deterministic isolation/recovery tests. Fake source, not a real-account trial."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import threading
import time
import unittest
from unittest.mock import patch
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

    def test_existing_login_connect_also_starts_inventory(self):
        _, session = self.new()
        original = session.backend.request
        def already_logged_in(method, path, body=None):
            if path.endswith('/qrcode'): return {'is_logged_in': True}
            return original(method, path, body)
        session.backend.request = already_logged_in
        session.start('connect', session.connect)
        until = time.monotonic() + 2
        while time.monotonic() < until and not session.library['items']: time.sleep(.02)
        self.assertEqual(len(session.library['items']), 1)
        self.assertEqual(session.state, 'connected')
        self.assertIsNone(session.qr)

    def test_existing_cookie_transient_failure_retries_without_qr(self):
        _, session = self.new(); session.backend.cookie_stamp = lambda: 123
        original = session.backend.request
        def unavailable(method, path, body=None):
            if path.endswith('/status'): raise S.Problem('source_unavailable', 502)
            return original(method, path, body)
        session.backend.request = unavailable
        with self.assertRaises(S.Problem): session.connect()
        self.assertFalse(any(call[1].endswith('/qrcode') for call in session.backend.calls))
        # Avoid status's first-restore auto-check in this deterministic test.
        session.checked_stamp = 123
        self.assertTrue(session.status()['canRetryVerification'])
        session.backend.request = original
        session.connect()
        self.assertEqual(session.state, 'connected')
        self.assertFalse(any(call[1].endswith('/qrcode') for call in session.backend.calls))

    def test_explicit_signed_out_cookie_can_obtain_qr(self):
        _, session = self.new(); session.backend.cookie_stamp = lambda: 123
        session.backend.logged = False
        session.connect()
        self.assertEqual(session.state, 'waiting')
        self.assertTrue(any(call[1].endswith('/qrcode') for call in session.backend.calls))

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

    def test_more_than_2000_saves_are_not_truncated(self):
        _, session = self.new(); session.verify()
        session.backend.profile = {'feeds': [card(f'{i:024x}') for i in range(2507)],
                                   'redbotScan': {'complete': True, 'endReason': 'source_end'}}
        session.scan()
        self.assertEqual(len(session.library['items']), 2507)
        self.assertEqual(session.library['scan']['seen'], 2507)
        self.assertTrue(session.library['scan']['complete'])
        self.assertEqual(session.library['scan']['coverage'], 'complete')

    def test_completion_requires_explicit_source_end(self):
        _, session = self.new(); session.verify()
        for marker in ({}, {'complete': False, 'endReason': 'stalled'}, {'complete': True, 'endReason': 'stalled'},
                       {'complete': False, 'endReason': 'source_response_incomplete'}):
            session.backend.profile = {'feeds': [card()], 'redbotScan': marker}
            session.scan()
            self.assertFalse(session.library['scan']['complete'])
            self.assertEqual(session.library['scan']['coverage'], 'partial')
        session.backend.profile = {'feeds': [], 'redbotScan': {'complete': True, 'endReason': 'source_end'}}
        session.scan()
        self.assertTrue(session.library['scan']['complete'])
        # A complete source scan still never erases locally retained saves.
        self.assertEqual(len(session.library['items']), 1)

    def test_streams_and_persists_batches_before_request_finishes(self):
        _, session = self.new(); session.verify()
        release, second = threading.Event(), threading.Event()
        original = session.backend.request
        def streaming(method, path, body=None):
            if not path.endswith('tab=fav'):
                return original(method, path, body)
            S.atomic(session.directory/'scan-checkpoint.json', {'feeds': [card()]})
            if not second.wait(3): raise AssertionError('test did not release second batch')
            S.atomic(session.directory/'scan-checkpoint.json', {'feeds': [card(), card(B)]})
            if not release.wait(3): raise AssertionError('test did not release request')
            raise S.Problem('source_unavailable', 502)
        session.backend.request = streaming
        session.start('scan', session.scan)
        def await_count(count):
            until = time.monotonic() + 2
            while time.monotonic() < until:
                if len(session.library['items']) == count: return
                time.sleep(.02)
            self.fail('batch did not become visible while request was running')
        try:
            await_count(1)
            first_revision = session.status()['revision']
            self.assertTrue(session.busy())
            self.assertEqual(len(S.read_json(session.directory/'library.json', {})['items']), 1)
            # A source touching/replacing an identical checkpoint must not
            # repeatedly persist the library or move the reader's card focus.
            S.atomic(session.directory/'scan-checkpoint.json', {'feeds': [card()]})
            time.sleep(.35)
            self.assertEqual(session.status()['revision'], first_revision)
            second.set(); await_count(2)
            self.assertGreater(session.status()['revision'], first_revision)
            self.assertEqual(session.status()['progress']['seen'], 2)
            self.assertTrue(session.library['scan']['running'])
        finally:
            second.set(); release.set()
        until = time.monotonic() + 2
        while session.busy() and time.monotonic() < until: time.sleep(.02)
        self.assertFalse(session.busy())
        self.assertTrue(session.library['scan']['interrupted'])
        self.assertFalse(session.library['scan']['running'])
        self.assertEqual(len(session.library['items']), 2)

    def test_cancel_scan_keeps_arrived_batch_and_allows_retry(self):
        _, session = self.new(); session.verify()
        stopped = threading.Event()
        original = session.backend.request
        def waiting(method, path, body=None):
            if not path.endswith('tab=fav'): return original(method, path, body)
            S.atomic(session.directory/'scan-checkpoint.json', {'feeds': [card()]})
            stopped.wait(3)
            raise S.Problem('source_unavailable', 502)
        session.backend.request = waiting
        session.backend.stop = stopped.set
        session.start('scan', session.scan)
        until = time.monotonic() + 2
        while not session.library['items'] and time.monotonic() < until: time.sleep(.02)
        self.assertEqual(len(session.library['items']), 1)
        session.cancel_scan()
        until = time.monotonic() + 2
        while session.busy() and time.monotonic() < until: time.sleep(.02)
        self.assertEqual(session.job['state'], 'cancelled')
        self.assertEqual(session.library['scan']['endReason'], 'cancelled')
        self.assertFalse(session.library['scan']['running'])
        self.assertEqual(len(session.library['items']), 1)
        session.backend.request = original
        session.start('scan', session.scan)
        until = time.monotonic() + 2
        while session.busy() and time.monotonic() < until: time.sleep(.02)
        self.assertEqual(session.job['state'], 'done')

    def test_restart_keeps_streamed_cards_but_does_not_claim_running(self):
        token, session = self.new(); session.verify(); session.scan()
        session.library['scan'].update(running=True, complete=False)
        revision = session.library['revision']
        S.atomic(session.directory/'library.json', session.library)
        restored = S.Store(Path(self.temp.name), Path('/unused'), factory=Fake).get(token)
        self.assertFalse(restored.library['scan']['running'])
        self.assertEqual(restored.library['scan']['endReason'], 'service_restarted')
        self.assertGreater(restored.library['revision'], revision)
        self.assertEqual(len(restored.library['items']), 1)

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

    def test_abandoned_trial_releases_capacity_and_can_sign_in_again(self):
        self.store.capacity = 1
        token, session = self.new()
        session.meta['pendingUntil'] = time.time() - 1
        replacement, fresh = self.new()
        self.assertNotEqual(token, replacement)
        self.assertFalse(session.directory.exists())
        with self.assertRaises(S.Problem) as error:
            self.store.get(token)
        self.assertEqual(error.exception.code, 'session_expired')
        fresh.connect()
        self.assertEqual(fresh.state, 'waiting')

    def test_recent_or_busy_pending_trial_is_kept(self):
        token, session = self.new()
        self.store.reap()
        self.assertIs(self.store.get(token), session)
        session.meta['pendingUntil'] = time.time() - 1
        session.job = {'state': 'running', 'kind': 'connect'}
        self.store.reap()
        self.assertIs(self.store.get(token), session)
        session.job['state'] = 'done'
        self.store.reap()
        self.assertFalse(session.directory.exists())

    def test_pending_expiry_never_evicts_identity_cookie_or_saved_items(self):
        sessions = [self.new() for _ in range(3)]
        sessions[0][1].meta['account'] = 'verified-account'
        sessions[1][1].backend.cookie_stamp = lambda: 123
        sessions[2][1].library['items'] = [{'id': A}]
        for _, session in sessions:
            session.meta['pendingUntil'] = time.time() - 1
        self.store.reap()
        for token, session in sessions:
            self.assertIs(self.store.get(token), session)
            self.assertTrue(session.directory.exists())

    def test_qr_start_refreshes_pending_clock_but_polling_does_not(self):
        _, session = self.new()
        deadline = session.meta['pendingUntil']
        self.assertEqual(session.status()['expiresAt'], deadline)
        session.status()
        self.assertEqual(session.meta['pendingUntil'], deadline)
        with patch.object(S.time, 'time', return_value=time.time() + 60):
            session.connect()
        self.assertGreater(session.meta['pendingUntil'], deadline + 59)
        persisted = S.read_json(session.directory / 'session.json', {})
        self.assertEqual(persisted['pendingUntil'], session.meta['pendingUntil'])

    def test_legacy_abandoned_trial_reaped_after_restart(self):
        token, session = self.new()
        session.meta.pop('pendingUntil')
        session.meta['createdAt'] = '2020-01-01T00:00:00Z'
        S.atomic(session.directory / 'session.json', session.meta)
        restored = S.Store(Path(self.temp.name), Path('/unused'), factory=Fake)
        restored.reap()
        self.assertFalse(session.directory.exists())
        with self.assertRaises(S.Problem):
            restored.get(token)

    def test_expired_pending_token_fails_without_waiting_for_next_signup(self):
        token, session = self.new()
        session.meta['pendingUntil'] = time.time() - 1
        with self.assertRaises(S.Problem) as error:
            self.store.get(token)
        self.assertEqual(error.exception.code, 'session_expired')
        self.assertFalse(session.directory.exists())

    def test_first_verification_promotes_to_normal_retention_only_once(self):
        _, session = self.new()
        now = time.time()
        with patch.object(S.time, 'time', return_value=now):
            session.verify()
        self.assertNotIn('pendingUntil', session.meta)
        self.assertEqual(session.meta['expires'], now + S.TTL)
        with patch.object(S.time, 'time', return_value=now + 60):
            session.verify()
        self.assertEqual(session.meta['expires'], now + S.TTL)
        # Reconnecting a bound account must not restart its seven-day window.
        session.state = 'needs_sign_in'
        session.backend.cookie_stamp = lambda: 123
        session.connect()
        self.assertEqual(session.meta['expires'], now + S.TTL)
        self.assertNotIn('pendingUntil', session.meta)

    def test_adapter_rejects_mutations_before_starting_process(self):
        mcp=S.MCP(Path('/missing'),Path(self.temp.name)/'new')
        with self.assertRaises(S.Problem):mcp.request('POST','/api/v1/feeds/favorite',{})
        self.assertIsNone(mcp.child)

    def test_private_connector_never_uses_system_proxy(self):
        class Source(S.BaseHTTPRequestHandler):
            def log_message(self, *_): pass
            def do_GET(self):
                body = json.dumps({'success': True, 'data': {'is_logged_in': False}}).encode()
                self.send_response(200); self.end_headers(); self.wfile.write(body)
        server = S.ThreadingHTTPServer(('127.0.0.1', 0), Source)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        mcp = S.MCP(Path('/unused'), Path(self.temp.name))
        mcp.port = server.server_port
        mcp.start = lambda: None
        try:
            with patch.dict(os.environ, {'http_proxy': 'http://127.0.0.1:1', 'HTTP_PROXY': 'http://127.0.0.1:1', 'no_proxy': '', 'NO_PROXY': ''}):
                self.assertFalse(mcp.request('GET', '/api/v1/login/status')['is_logged_in'])
        finally:
            server.shutdown(); server.server_close()

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
