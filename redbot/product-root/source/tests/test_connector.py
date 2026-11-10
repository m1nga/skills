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
            return {'feed_id': body['feed_id'], 'data': {'note': {'noteId': body['feed_id'], 'desc': 'Original text', 'title': 'A free tool'}, 'comments': {}}}
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

    def test_default_account_store_accepts_more_than_three_without_evicting_existing(self):
        with tempfile.TemporaryDirectory() as folder:
            store = S.Store(Path(folder), Path('/unused'), factory=Fake)
            try:
                connections = [store.create(store.config['invite'], True) for _ in range(5)]
                self.assertEqual(len(store.sessions), 5)
                self.assertEqual(len({x['sessionId'] for x in connections}), 5)
                for connection in connections:
                    self.assertEqual(store.get(connection['token']).meta['id'], connection['sessionId'])
            finally:
                store.stop()

    def test_explicit_account_quota_remains_an_operator_option(self):
        for _ in range(3): self.new()
        with self.assertRaises(S.Problem) as error: self.new()
        self.assertEqual(error.exception.code, 'beta_full')

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

    def test_pinned_go_http_envelope_reaches_selected_read(self):
        _, session = self.new(); session.verify(); session.scan()
        requests = []
        class Source(S.BaseHTTPRequestHandler):
            def log_message(self, *_): pass
            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                requests.append((self.path, body))
                payload = {'success': True, 'data': {'feed_id': A, 'data': {
                    'note': {'noteId': A, 'desc': 'Body from Go envelope', 'title': 'Read title', 'type': 'normal'},
                    'comments': {'list': [], 'hasMore': False}}}}
                self.send_response(200); self.end_headers(); self.wfile.write(json.dumps(payload).encode())
        server = S.ThreadingHTTPServer(('127.0.0.1', 0), Source)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        mcp = S.MCP(Path('/unused'), session.directory); mcp.port = server.server_port; mcp.start = lambda: None
        try:
            with patch.object(session, 'verify'):
                session.backend = mcp
                session.start('read', lambda: session.read(A), A); session.worker.join(2)
            self.assertEqual(session.job['state'], 'done'); self.assertEqual(session.job['targetId'], A)
            self.assertEqual(requests, [('/api/v1/feeds/detail', {'feed_id': A, 'xsec_token': 'private-source-token', 'load_all_comments': False})])
            item = session.library['items'][0]
            self.assertEqual(item['description'], 'Body from Go envelope'); self.assertEqual(item['contentReadStatus'], 'ready')
            self.assertEqual(session.library['scan']['readCount'], 1)
        finally:
            server.shutdown(); server.server_close()

    def test_invalid_or_failed_refresh_retains_successful_body(self):
        _, session = self.new(); session.verify(); session.scan(); session.read(A)
        item = session.library['items'][0]; original_time = item['contentReadAt']
        cases = [None, {'data': {'note': {'noteId': '', 'desc': ''}}},
                 {'data': {'note': {'noteId': B, 'desc': 'Wrong post'}}},
                 {'feed_id': B, 'data': {'note': {'noteId': A, 'desc': 'Wrong envelope'}}}]
        for payload in cases:
            with patch.object(session.backend, 'request', return_value=payload), patch.object(session, 'verify'):
                with self.assertRaises(S.Problem) as error: session.read(A)
            self.assertEqual(error.exception.code, 'source_content_invalid')
            self.assertEqual(item['description'], 'Original text'); self.assertEqual(item['contentReadAt'], original_time)
            self.assertEqual(item['contentReadStatus'], 'failed'); self.assertTrue(item['contentReadError']['retainedPrevious'])
        with patch.object(session.backend, 'request', side_effect=S.Problem('source_unavailable', 502)), patch.object(session, 'verify'):
            session.start('read', lambda: session.read(A), A); session.worker.join(2)
        self.assertEqual(session.job['state'], 'failed'); self.assertEqual(session.job['error'], 'source_unavailable')
        self.assertEqual(item['description'], 'Original text'); self.assertEqual(item['contentReadAt'], original_time)

    def test_legitimate_empty_caption_has_explicit_status(self):
        _, session = self.new(); session.verify(); session.scan()
        with patch.object(session.backend, 'request', return_value={'feed_id': A, 'data': {'note': {'noteId': A, 'desc': ''}}}), patch.object(session, 'verify'):
            session.read(A)
        item = session.library['items'][0]
        self.assertEqual(item['contentReadStatus'], 'empty'); self.assertFalse(item['hasContent'])
        self.assertEqual(item['coverage'], 'post_text_empty'); self.assertNotIn('contentReadError', item)
        self.assertEqual(session.library['scan']['readCount'], 0)

    def test_missing_token_does_not_request_detail(self):
        _, session = self.new(); session.verify(); session.scan()
        S.atomic(session.directory / 'source-tokens.json', {})
        with patch.object(session.backend, 'request') as request, patch.object(session, 'verify'):
            with self.assertRaises(S.Problem) as error: session.read(A)
        self.assertEqual(error.exception.code, 'sync_first'); request.assert_not_called()
        self.assertEqual(session.library['items'][0]['contentReadError']['code'], 'sync_first')

    def test_cancel_selected_read_prevents_late_source_commit(self):
        _, session = self.new(); session.verify(); session.scan(); session.read(A)
        entered, release = threading.Event(), threading.Event()
        previous_comments = {'items': [{'text': 'Previously read', 'isAuthor': True}], 'scope': 'first_page_returned'}
        session.library['items'][0]['comments'] = previous_comments
        def detail(*args):
            entered.set(); release.wait(2)
            return {'feed_id': A, 'data': {'note': {'noteId': A, 'desc': 'Late body'}, 'comments': {'list': [{'content': 'Late comment'}]}}}
        with patch.object(session.backend, 'request', side_effect=detail), patch.object(session, 'verify'):
            session.start('read', lambda: session.read(A), A); self.assertTrue(entered.wait(1))
            self.assertEqual(session.cancel_read(), {'cancelRequested': True}); release.set(); session.worker.join(2)
        self.assertEqual(session.job['state'], 'cancelled'); self.assertEqual(session.job['targetId'], A)
        item = session.library['items'][0]
        self.assertEqual(item['description'], 'Original text'); self.assertEqual(item['contentReadStatus'], 'cancelled')
        self.assertEqual(item['contentReadError']['code'], 'read_cancelled')
        self.assertEqual(item['comments'], previous_comments)

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

    def test_cancel_video_during_source_failure_persists_cancelled_status(self):
        _, session = self.new(); session.verify(); session.scan()
        item = session.library['items'][0]; item['type'] = 'video'
        previous_comments = {'items': [{'text': 'Previous video comment', 'isAuthor': True}], 'scope': 'first_page_returned'}
        item['comments'] = previous_comments
        entered, release = threading.Event(), threading.Event()
        def detail(*args):
            entered.set(); release.wait(2)
            return {'feed_id': A, 'data': {'note': {'noteId': A, 'desc': 'Late caption'}, 'comments': {'list': [{'content': 'Late video comment'}]}}}
        with patch.object(session.backend, 'request', side_effect=detail), patch.object(session, 'verify'):
            session.start('video', lambda: session.read_video(A), A); self.assertTrue(entered.wait(1))
            session.cancel_video(); release.set(); session.worker.join(2)
        self.assertEqual(session.job['state'], 'cancelled')
        self.assertEqual(item['contentReadStatus'], 'cancelled')
        self.assertEqual(item['contentReadError']['code'], 'video_cancelled')
        self.assertEqual(item['comments'], previous_comments)

    def test_restart_turns_inflight_read_into_recoverable_failure(self):
        token, session = self.new(); session.verify(); session.scan(); session.read(A)
        item = session.library['items'][0]; item['contentReadStatus'] = 'running'
        S.atomic(session.directory / 'library.json', session.library)
        restored = S.Store(Path(self.temp.name), Path('/unused'), factory=Fake).get(token)
        recovered = restored.library['items'][0]
        self.assertEqual(recovered['contentReadStatus'], 'failed')
        self.assertEqual(recovered['contentReadError']['code'], 'service_restarted')
        self.assertTrue(recovered['contentReadError']['retainedPrevious'])
        self.assertEqual(recovered['description'], 'Original text')

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


    def test_large_private_library_compression_preserves_content_and_auth(self):
        import gzip
        token, session = self.new(); session.verify(); session.scan()
        session.library['items'][0]['description'] = '原始收藏内容与个人方法。' * 2000
        server = S.ThreadingHTTPServer(('127.0.0.1', 0), S.BaseHTTPRequestHandler)
        host = '127.0.0.1:' + str(server.server_port)
        server.RequestHandlerClass = S.make_handler(self.store, {'https://sidecourt.space'}, host)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            for encoding in ['gzip', 'identity', 'gzip;q=0']:
                headers = {'Authorization': 'Bearer ' + token, 'Origin': 'https://sidecourt.space', 'Accept-Encoding': encoding}
                with urlopen(Request('http://' + host + '/api/library', headers=headers)) as response:
                    body = response.read()
                    self.assertEqual(len(body), int(response.headers['Content-Length']))
                    self.assertEqual(response.headers['Access-Control-Allow-Origin'], 'https://sidecourt.space')
                    self.assertIn('Accept-Encoding', response.headers['Vary'])
                    if encoding == 'gzip':
                        self.assertEqual(response.headers['Content-Encoding'], 'gzip')
                        decoded = gzip.decompress(body)
                        self.assertLess(len(body), len(decoded) // 2)
                    else:
                        self.assertIsNone(response.headers.get('Content-Encoding'))
                        decoded = body
                    self.assertEqual(json.loads(decoded)['items'][0]['description'], session.library['items'][0]['description'])
            with self.assertRaises(HTTPError) as error:
                urlopen(Request('http://' + host + '/api/library', headers={'Accept-Encoding': 'gzip'}))
            self.assertEqual(error.exception.code, 401)
        finally:
            server.shutdown(); server.server_close()

    def test_returned_first_page_comments_are_bounded_and_identity_free(self):
        author = {'userId': 'private-author', 'nickname': 'not copied'}
        comment = {'id': 'private-comment', 'noteId': A, 'content': 'A concrete method',
                   'userInfo': author, 'ipLocation': 'not copied',
                   'subComments': [{'content': 'A reader reply', 'userInfo': {'userId': 'private-reader'}}]}
        note = {'noteId': A, 'desc': 'caption', 'user': author}
        out = {'data': {'note': note, 'comments': {'list': [comment], 'hasMore': True, 'cursor': 'private-cursor'}}}
        result = S.detail_comments(out, note, A)
        self.assertEqual(result['scope'], 'first_page_returned')
        self.assertTrue(result['hasMore'])
        self.assertEqual(result['items'], [{'text': 'A concrete method', 'isAuthor': True, 'reply': False},
                                           {'text': 'A reader reply', 'isAuthor': False, 'reply': True}])
        self.assertNotIn('private-', json.dumps(result))
        self.assertIsNone(S.detail_comments({'data': {}}, note, A))
        out['data']['comments']['list'] = [{'noteId': B, 'content': 'Wrong note'}, *[{'content': 'x' * 8000}] * 50]
        result = S.detail_comments(out, note, A)
        self.assertTrue(result['truncated'])
        self.assertLessEqual(sum(len(c['text']) for c in result['items']), 30000)
        self.assertTrue(all(len(c['text']) <= 4000 for c in result['items']))
        self.assertNotIn('Wrong note', json.dumps(result))

    def test_selected_read_keeps_only_already_returned_first_page_comments(self):
        _, session = self.new(); session.verify(); session.scan()
        original = session.backend.request
        def response(method, path, body=None):
            out = original(method, path, body)
            if path.endswith('/detail'):
                out['data']['note']['user'] = {'userId': 'author'}
                out['data']['comments'] = {'list': [{'content': 'Useful original author method', 'userInfo': {'userId': 'author'}}], 'hasMore': True}
            return out
        with patch.object(session.backend, 'request', side_effect=response):
            session.read(A)
        comments = session.library['items'][0]['comments']
        self.assertTrue(comments['items'][0]['isAuthor'])
        self.assertTrue(comments['hasMore'])
        detail_calls = [c for c in session.backend.calls if c[1].endswith('/detail')]
        self.assertEqual(len(detail_calls), 1)
        self.assertFalse(detail_calls[0][2]['load_all_comments'])


if __name__=='__main__':unittest.main()
