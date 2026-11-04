"""Reading across a library, with failures and process restart (fake source)."""
import json
from pathlib import Path
import tempfile
import threading
import time
import unittest
from unittest.mock import patch
from test_connector import S, Fake, card, A, B


class ReadingQueueTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = S.Store(Path(self.temp.name), Path('/unused'), factory=Fake)
        self.token = self.store.create(self.store.config['invite'], True)['token']
        self.session = self.store.get(self.token)
        self.session.verify()

    def tearDown(self):
        self.store.stop()
        self.temp.cleanup()

    def wait(self):
        self.session.queue_worker.join(5)
        self.assertFalse(self.session.queue_worker.is_alive())

    def test_all_saves_eligible_without_count_cap_and_resume_keeps_queue(self):
        session = self.session
        session.backend.profile = {'feeds': [card(f'{i:024x}') for i in range(2507)]}
        session.scan()
        with patch.object(threading.Thread, 'start'):
            status = session.read_all()
        self.assertEqual(status['remaining'], 2507)
        self.assertEqual(status['total'], 2507)
        session.pause_reading()
        restored = S.Session(session.directory, session.meta, Fake(None, session.directory))
        restored.state = 'connected'
        self.assertEqual(restored.queue_status()['remaining'], 2507)
        self.assertEqual(restored.queue_status()['state'], 'paused')
        with patch.object(threading.Thread, 'start'):
            self.assertEqual(restored.read_all()['remaining'], 2507)

    def test_failure_does_not_block_next_post_and_read_results_are_not_repeated(self):
        session = self.session
        session.backend.profile = {'feeds': [card(A), card(B), card('c'*24)]}
        session.scan()
        session.read('c'*24)
        original = session.backend.request
        def request(method, path, body=None):
            if path.endswith('/detail') and body['feed_id'] == A:
                raise S.Problem('source_unavailable', 502)
            return original(method, path, body)
        session.backend.request = request
        # Skip only the two-second pacing, not the actual worker or source flow.
        with patch.object(session.queue_stop, 'wait', return_value=False):
            session.read_all(); self.wait()
        status = session.queue_status()
        self.assertEqual((status['done'], status['failed'], status['remaining']), (2, 1, 0))
        before = len(session.backend.calls)
        session.read_all()
        self.assertEqual(len(session.backend.calls), before)
        session.backend.request = original
        with patch.object(session.queue_stop, 'wait', return_value=False):
            session.read_all(retry_failed=True); self.wait()
        self.assertEqual(session.queue_status()['done'], 3)
        calls = [c for c in session.backend.calls if c[1].endswith('/detail')]
        self.assertEqual([c[2]['feed_id'] for c in calls].count('c'*24), 1)

    def test_refresh_preserves_pause_and_results_then_resume_includes_new_saves(self):
        session = self.session
        session.backend.profile = {'feeds': [card(A), card(B)]}
        session.scan(); session.read(A)
        with patch.object(threading.Thread, 'start'): session.read_all()
        session.pause_reading()
        session.backend.profile = {'feeds': [card(A), card(B), card('c'*24)]}
        session.scan()
        self.assertEqual(session.queue_status()['state'], 'paused')
        self.assertEqual(session.queue_status()['done'], 1)
        restored = S.Session(session.directory, session.meta, Fake(None, session.directory))
        restored.state = 'connected'
        self.assertEqual(restored.queue_status()['state'], 'paused')
        with patch.object(threading.Thread, 'start'): status = restored.read_all()
        self.assertEqual((status['total'], status['done'], status['remaining']), (3, 1, 2))
        self.assertEqual(restored.library['readingQueue']['pending'], [B, 'c'*24])

    def test_pause_finishes_current_and_restart_does_not_silently_restart(self):
        session = self.session
        session.backend.profile = {'feeds': [card(A), card(B)]}; session.scan()
        entered, release = threading.Event(), threading.Event()
        original = session.backend.request
        def request(method, path, body=None):
            if path.endswith('/detail'):
                entered.set(); release.wait(3)
            return original(method, path, body)
        session.backend.request = request
        session.read_all(); self.assertTrue(entered.wait(1))
        session.pause_reading(); release.set(); self.wait()
        self.assertEqual(session.queue_status()['state'], 'paused')
        self.assertEqual(session.queue_status()['remaining'], 1)
        session.library['readingQueue']['state'] = 'running'; session.save_queue()
        restored = S.Session(session.directory, session.meta, Fake(None, session.directory))
        self.assertEqual(restored.queue_status()['state'], 'paused')
        self.assertEqual(restored.queue_status()['remaining'], 1)
        self.assertEqual(restored.backend.calls, [])

    def test_signed_out_queue_pauses_and_other_accounts_are_untouched(self):
        session = self.session
        session.backend.profile = {'feeds': [card(A), card(B)]}; session.scan()
        other = self.store.get(self.store.create(self.store.config['invite'], True)['token'])
        session.backend.logged = False
        with patch.object(session.queue_stop, 'wait', return_value=False):
            session.read_all(); self.wait()
        self.assertEqual(session.queue_status()['state'], 'paused')
        self.assertEqual(session.queue_status()['remaining'], 1)
        self.assertEqual(other.library['items'], [])
        self.assertEqual(other.backend.calls, [])

    def test_video_failure_keeps_caption_and_comments(self):
        session = self.session; session.backend.profile = {'feeds': [card(A)]}; session.scan()
        item = session.library['items'][0]; item['type'] = 'video'
        with patch.object(S.video, 'analyze', side_effect=S.video.VideoError('video_download_failed')):
            with self.assertRaises(S.Problem): session.read_video(A)
        self.assertEqual(item['description'], 'Original text')
        self.assertEqual(item['contentReadStatus'], 'failed')
        self.assertTrue(item['contentReadAt'])
        self.assertFalse(S.Session.content_complete(item))

    def test_opened_save_moves_next_without_interrupting_current_or_borrowing_another_library(self):
        session=self.session
        session.backend.profile={'feeds':[card(A),card(B),card('c'*24)]};session.scan()
        with patch.object(threading.Thread,'start'):session.read_all()
        session.library['readingQueue']['currentId']=A
        session.prioritize_read('c'*24)
        self.assertEqual(session.library['readingQueue']['pending'],[A,'c'*24,B])
        session.prioritize_read('c'*24)
        self.assertEqual(session.library['readingQueue']['pending'],[A,'c'*24,B])
        with self.assertRaises(S.Problem):session.prioritize_read('d'*24)
