"""RedBot's invite-only read connector with opt-in local ASR/OCR inference.

No cloud inference, shared owner session, or source write tool.

Each visitor gets a separate MCP process, cookie file, private library and bearer.
The HTTP server binds to loopback. An operator may explicitly place an HTTPS proxy
in front of it; only the app's configured origins are accepted. Runtime is outside
the source tree. This is a small test service, not an always-on hosting platform.
"""
from __future__ import annotations

import argparse
import base64
import calendar
import hashlib
import hmac
import json
import os
from pathlib import Path
import re
import secrets
import shutil
import signal
import socket
import subprocess
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.error import HTTPError, URLError
from urllib.request import Request, build_opener, ProxyHandler
from urllib.parse import unquote

APP = Path(__file__).resolve().parents[1] / 'app'
ID = re.compile(r'^[a-f0-9]{24}$')
TTL = 7 * 86400
PENDING_TTL = 20 * 60
VIDEO_SLOT = threading.BoundedSemaphore(1)
# The source process lives on loopback. Never forward its bearer or health
# request through a shell/system HTTP proxy (macOS can supply one implicitly).
_local_http = build_opener(ProxyHandler({}))


try:
    from . import video
except ImportError:
    import importlib.util
    _video_spec = importlib.util.spec_from_file_location("redbot_video", Path(__file__).with_name("video.py"))
    video = importlib.util.module_from_spec(_video_spec)
    _video_spec.loader.exec_module(video)


class Problem(Exception):
    def __init__(self, code, status=400):
        super().__init__(code)
        self.code, self.status = code, status


def atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    temp = path.with_suffix('.tmp')
    with open(temp, 'w', encoding='utf-8') as f:
        os.chmod(temp, 0o600)
        json.dump(data, f, ensure_ascii=False)
    temp.replace(path)


def read_json(path, default):
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return default


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


def iso():
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


def merge_scan(previous, profile):
    """Only source fields change. Missing cards never imply an unsave/deletion."""
    old = {x['id']: x for x in previous.get('items', [])}
    result, tokens, seen = [], {}, set()
    added = changed = unchanged = 0
    for row in profile.get('feeds', []):
        nid = row.get('id', '')
        if not ID.fullmatch(nid) or nid in seen:
            continue
        seen.add(nid)
        card = row.get('noteCard', {})
        source = {
            'title': card.get('displayTitle') or old.get(nid, {}).get('title') or 'Untitled save',
            'author': card.get('user', {}).get('nickname', ''),
            'image': (card.get('cover', {}).get('urlDefault') or card.get('cover', {}).get('url') or '').replace('http://', 'https://'),
            'type': 'video' if card.get('type') == 'video' else 'note',
        }
        # Signed cover URLs may rotate without a content change. Track title,
        # author and kind; detailed text remains an explicit selected-source read.
        fingerprint = digest(json.dumps({k: source[k] for k in ('title', 'author', 'type')}, sort_keys=True))
        prior = old.get(nid, {})
        added += not bool(prior)
        changed += bool(prior) and prior.get('sourceFingerprint') != fingerprint
        unchanged += bool(prior) and prior.get('sourceFingerprint') == fingerprint
        item = {**prior, **source, 'id': nid, 'url': 'https://www.xiaohongshu.com/explore/' + nid,
                'position': len(result), 'sourceFingerprint': fingerprint,
                'importedAt': prior.get('importedAt', iso()), 'lastSeenAt': iso()}
        if prior and prior.get('sourceFingerprint') != fingerprint:
            item['sourceMayHaveChanged'] = True
        result.append(item)
        if row.get('xsecToken'):
            tokens[nid] = row['xsecToken']
    result.extend(x for x in old.values() if x['id'] not in seen)
    return {
        'version': 1, 'items': result,
        'scan': {'at': iso(), 'count': len(seen), 'added': added, 'changed': changed,
                 'unchanged': unchanged, 'kept': len(old.keys() - seen),
                 'complete': False, 'coverage': 'partial',
                 'llmTokens': 0, 'readCount': sum(bool(x.get('description')) for x in result),
                 'analyzedCount': 0},
    }, tokens


def detail_note(out, nid):
    """Decode the pinned HTTP service result after MCP strips success/data."""
    if not isinstance(out, dict):
        raise Problem('source_content_invalid', 502)
    if out.get('feed_id', nid) != nid:
        raise Problem('source_content_invalid', 502)
    content = out.get('data', out)
    note = content.get('note') if isinstance(content, dict) else None
    if not isinstance(note, dict) or note.get('noteId') != nid or not isinstance(note.get('desc'), str):
        raise Problem('source_content_invalid', 502)
    return note


def detail_comments(out, note, nid):
    """Only the already-returned first page; never persist commenter IDs or cursors."""
    content = out.get('data', out)
    raw = content.get('comments') if isinstance(content, dict) else None
    if not isinstance(raw, dict) or not isinstance(raw.get('list'), list):
        return None
    author = note.get('user', {}).get('userId') if isinstance(note.get('user'), dict) else None
    rows, budget, truncated = [], 30000, False
    def keep(comment, reply=False):
        nonlocal budget, truncated
        if not isinstance(comment, dict) or comment.get('noteId', nid) != nid:
            return
        text = comment.get('content')
        if not isinstance(text, str) or not text.strip():
            return
        text = text.strip()
        if len(text) > 4000 or len(text) > budget:
            truncated = True
        text = text[:min(4000, budget)]
        if not text:
            return
        user = comment.get('userInfo')
        uid = user.get('userId') if isinstance(user, dict) else None
        rows.append({'text': text, 'isAuthor': uid == author if uid and author else None,
                     'reply': reply})
        budget -= len(text)
    for comment in raw['list'][:20]:
        keep(comment)
        if isinstance(comment, dict):
            replies = comment.get('subComments')
            if isinstance(replies, list):
                for reply in replies[:3]:
                    keep(reply, True)
                truncated = truncated or len(replies) > 3
    return {'items': rows, 'scope': 'first_page_returned', 'hasMore': raw.get('hasMore') if isinstance(raw.get('hasMore'), bool) else None,
            'truncated': truncated or len(raw['list']) > 20, 'readAt': iso()}


class MCP:
    """A private process, never a connection to a pre-existing owner MCP port."""
    def __init__(self, binary, directory):
        self.binary, self.directory = str(binary), directory
        self.child = None
        self.port = None
        self.token = secrets.token_urlsafe(32)
        self.lock = threading.RLock()
        self.log = None

    def start(self):
        if getattr(self, 'disabled', False):
            raise Problem('session_expired', 401)
        if self.child and self.child.poll() is None:
            return
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0))
            self.port = sock.getsockname()[1]
        env = os.environ.copy()
        # Never inherit a caller's account path, auth token, or proxy setting.
        for key in ('AUTH_TOKEN', 'COOKIES_PATH', 'XHS_FP_SEED', 'XHS_PROXY'):
            env.pop(key, None)
        env.update(AUTH_TOKEN=self.token, COOKIES_PATH=str(self.directory / 'cookies.json'),
                   REDBOT_SCAN_CHECKPOINT=str(self.directory / 'scan-checkpoint.json'))
        self.directory.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.log = open(self.directory / 'connector.log', 'ab')
        os.chmod(self.directory / 'connector.log', 0o600)
        self.child = subprocess.Popen(
            [self.binary, '-headless=true', '-port', f'127.0.0.1:{self.port}'],
            cwd=self.directory, env=env, stdout=self.log, stderr=self.log,
            start_new_session=True, umask=0o077)
        for _ in range(100):
            if self.child.poll() is not None:
                raise Problem('connector_unavailable', 503)
            try:
                with _local_http.open(f'http://127.0.0.1:{self.port}/health', timeout=0.3) as response:
                    if response.status == 200:
                        return
            except (OSError, URLError):
                time.sleep(0.1)
        self.stop()
        raise Problem('connector_unavailable', 503)

    def request(self, method, path, body=None):
        allowed = {('GET', '/api/v1/login/qrcode'), ('GET', '/api/v1/login/status'),
                   ('GET', '/api/v1/user/me?tab=fav'), ('POST', '/api/v1/feeds/detail')}
        if (method, path) not in allowed:
            raise Problem('read_only', 403)
        with self.lock:
            self.start()
            req = Request(f'http://127.0.0.1:{self.port}' + path,
                          data=json.dumps(body).encode() if body is not None else None,
                          headers={'Authorization': 'Bearer ' + self.token, 'Content-Type': 'application/json'},
                          method=method)
            try:
                # Inventory streams through the private checkpoint while this
                # request remains open. Its deadline is time, not card count.
                timeout = 1830 if path == '/api/v1/user/me?tab=fav' else 190
                with _local_http.open(req, timeout=timeout) as response:
                    out = json.load(response)
            except HTTPError as error:
                # Diagnostics stay in this private account directory, not in a
                # browser response or public report. Successful source text is
                # never logged here.
                try:
                    detail = json.loads(error.read(12000))
                    atomic(self.directory / 'last-error.json', {'at':iso(),'path':path,'status':error.code,'diagnostic':detail})
                except (OSError, ValueError):
                    pass
                raise Problem('source_unavailable', 502)
            except (OSError, ValueError, URLError):
                # Upstream details can contain tokens/URLs; never forward them.
                raise Problem('source_unavailable', 502)
            if out.get('success') is not True:
                raise Problem('source_unavailable', 502)
            return out.get('data', {})

    def cookie_stamp(self):
        p = self.directory / 'cookies.json'
        data = read_json(p, {})
        cookies = data if isinstance(data, list) else data.get('cookies', [])
        return p.stat().st_mtime_ns if cookies else None

    def stop(self):
        child, self.child = self.child, None
        if child and child.poll() is None:
            try:
                os.killpg(child.pid, signal.SIGTERM)
                child.wait(timeout=5)
            except (ProcessLookupError, subprocess.TimeoutExpired):
                try:
                    os.killpg(child.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
        if self.log:
            self.log.close()
            self.log = None


class Session:
    def __init__(self, directory, meta, backend):
        self.directory, self.meta, self.backend = directory, meta, backend
        self.lock = threading.RLock()
        self.job = None
        self.qr = None
        self.qr_expires = 0
        self.checked_stamp = None
        self.state = 'needs_sign_in'
        self.closed = False
        self.scan_started = None
        self.scan_cancel = threading.Event()
        self.video_cancel = threading.Event()
        self.read_cancel = threading.Event()
        self.library = read_json(directory / 'library.json', {'version': 1, 'items': []})
        self.library.setdefault('revision', 0)
        interrupted_reads = False
        for item in self.library['items']:
            if item.get('contentReadStatus') == 'running':
                item.update(contentReadStatus='failed', contentReadError={
                    'code': 'service_restarted', 'at': iso(),
                    'retainedPrevious': bool(item.get('contentReadAt'))})
                interrupted_reads = True
        if interrupted_reads:
            self.library['revision'] += 1
            atomic(directory / 'library.json', self.library)
        if self.library.get('scan', {}).get('running'):
            self.library['scan'].update(running=False, complete=False, coverage='partial',
                                        interrupted=True, endReason='service_restarted')
            self.library['revision'] += 1
            atomic(directory / 'library.json', self.library)

    def pending_deadline(self):
        # Legacy trials had a seven-day expiry. Use their original creation time,
        # never passive status polling, as the fallback QR-flow clock.
        if 'pendingUntil' in self.meta:
            return self.meta['pendingUntil']
        try:
            return calendar.timegm(time.strptime(self.meta['createdAt'], '%Y-%m-%dT%H:%M:%SZ')) + PENDING_TTL
        except (KeyError, ValueError, TypeError):
            return self.meta['expires']

    def expires_at(self):
        if self.meta.get('account') or self.library.get('items') or self.backend.cookie_stamp():
            return self.meta['expires']
        return min(self.meta['expires'], self.pending_deadline())

    def abandoned(self):
        return (not self.meta.get('account') and not self.library.get('items')
                and not self.busy() and not self.backend.cookie_stamp()
                and self.pending_deadline() <= time.time())

    def status(self):
        with self.lock:
            if self.state == 'waiting' and time.time() >= self.qr_expires:
                self.state, self.qr = 'expired', None
                self.backend.stop()
            stamp = self.backend.cookie_stamp()
            if self.state in ('waiting', 'needs_sign_in') and stamp and stamp != self.checked_stamp and not self.busy():
                self.checked_stamp = stamp
                self.start('verify', self.verify)
            progress = None
            scan = self.library.get('scan', {})
            if self.busy() and self.job['kind'] == 'scan':
                progress = {key: scan.get(key) for key in ('seen', 'complete', 'endReason')}
                progress.update(revision=self.library['revision'], running=True)
            return {'state': self.state, 'nickname': self.meta.get('nickname', ''),
                    'sessionId': self.meta['id'], 'expiresAt': self.expires_at(),
                    'qr': self.qr if self.state == 'waiting' else None,
                    'qrExpiresAt': self.qr_expires, 'job': self.job,
                    'scan': self.library.get('scan'), 'progress': progress,
                    'revision': self.library['revision'], 'items': len(self.library['items']),
                    'canRetryVerification': bool(stamp and self.state in ('needs_sign_in', 'expired') and not self.busy())}

    def busy(self):
        return bool(self.job and self.job['state'] == 'running')

    def start(self, kind, fn, target_id=None):
        with self.lock:
            if self.closed:
                raise Problem('session_expired', 401)
            if self.busy():
                raise Problem('busy', 409)
            if kind == 'video' and not VIDEO_SLOT.acquire(blocking=False):
                raise Problem('video_busy', 429)
            job_id = secrets.token_hex(10)
            if kind == 'read':
                self.read_cancel.clear()
            if kind == 'scan':
                self.scan_cancel.clear()
            if kind == 'video':
                self.video_cancel.clear()
            self.job = {'id': job_id, 'kind': kind, 'state': 'running', 'startedAt': iso()}
            if target_id is not None:
                self.job['targetId'] = target_id

        def run():
            try:
                fn()
                with self.lock:
                    if self.closed:
                        return
                    self.job = {**self.job, 'state': 'cancelled' if (kind == 'scan' and self.scan_cancel.is_set() or kind == 'video' and self.video_cancel.is_set() or kind == 'read' and self.read_cancel.is_set()) else 'done', 'finishedAt': iso()}
                if kind in ('verify', 'connect') and self.state == 'connected':
                    self.start('scan', self.scan)
            except Exception as e:
                with self.lock:
                    if not self.closed:
                        self.job = {**self.job, 'state': 'cancelled' if (kind == 'scan' and self.scan_cancel.is_set() or kind == 'video' and self.video_cancel.is_set() or kind == 'read' and self.read_cancel.is_set()) else 'failed',
                                    'error': ('video_cancelled' if kind == 'video' else 'read_cancelled' if kind == 'read' else 'scan_cancelled') if (kind == 'scan' and self.scan_cancel.is_set() or kind == 'video' and self.video_cancel.is_set() or kind == 'read' and self.read_cancel.is_set()) else e.code if isinstance(e, Problem) else 'source_unavailable'}
            finally:
                if kind == 'video':
                    VIDEO_SLOT.release()
        worker = threading.Thread(target=run, daemon=True)
        self.worker = worker
        worker.start()
        return {'jobId': job_id}

    def connect(self):
        if self.closed:
            raise Problem('session_expired', 401)
        if self.state == 'connected':
            raise Problem('already_connected', 409)
        with self.lock:
            if not self.meta.get('account'):
                self.meta['pendingUntil'] = time.time() + PENDING_TTL
                atomic(self.directory / 'session.json', self.meta)
        self.qr = None
        # Restoring an existing session is an identity check, not a request to
        # discard login and issue a fresh QR. Transient loading failures remain
        # retryable. Only a confirmed signed-out response advances to QR login.
        if self.backend.cookie_stamp():
            try:
                self.verify()
                return
            except Problem as error:
                if error.code != 'sign_in_required':
                    raise
        out = self.backend.request('GET', '/api/v1/login/qrcode')
        if out.get('is_logged_in'):
            self.verify()
            return
        img = out.get('img', '')
        if not re.fullmatch(r'data:image/(png|jpeg);base64,[A-Za-z0-9+/=\r\n]+', img) or len(img) > 2_000_000:
            raise Problem('qr_unavailable', 502)
        with self.lock:
            if self.closed:
                raise Problem('session_expired', 401)
            self.state, self.qr, self.qr_expires = 'waiting', img, time.time() + 230

    def verify(self):
        if self.closed:
            raise Problem('session_expired', 401)
        out = self.backend.request('GET', '/api/v1/login/status')
        uid = out.get('user_id') or out.get('userId')
        if not out.get('is_logged_in') or not uid:
            self.state = 'needs_sign_in'
            raise Problem('sign_in_required', 401)
        account = digest(str(uid))
        # A reconnect cannot merge a different account into the old library.
        if self.meta.get('account') and self.meta['account'] != account:
            self.state, self.qr = 'wrong_account', None
            self.backend.stop()
            raise Problem('wrong_account', 409)
        with self.lock:
            if self.closed:
                raise Problem('session_expired', 401)
            first_verification = not self.meta.get('account')
            self.meta.update(account=account, nickname=str(out.get('username', ''))[:120])
            if first_verification:
                # Start the normal account retention window at first verification.
                self.meta['expires'] = time.time() + TTL
                self.meta.pop('pendingUntil', None)
            atomic(self.directory / 'session.json', self.meta)
            self.state, self.qr = 'connected', None

    def scan(self):
        if self.state != 'connected':
            raise Problem('sign_in_required', 401)
        # Check identity on every scan, including after a service restart.
        self.verify()
        if self.scan_cancel.is_set():
            raise Problem('scan_cancelled', 409)
        self.scan_started = time.time()
        checkpoint = self.directory / 'scan-checkpoint.json'
        checkpoint.unlink(missing_ok=True)
        stop_monitor = threading.Event()
        baseline = self.library
        latest = None
        checkpoint_stamp = None
        checkpoint_content = None

        def publish(profile, running, reason=None):
            nonlocal latest
            if profile.get('feeds') is None and isinstance(profile.get('userBasicInfo'), dict):
                profile = {**profile, 'feeds': []}
            if not isinstance(profile.get('feeds'), list):
                raise Problem('scan_incomplete', 502)
            source_scan = profile.get('redbotScan') or {}
            # Only the adapter's observed, successful final pagination response
            # proves completeness. A quiet/stalled DOM never does.
            complete = not running and not reason and source_scan.get('complete') is True and source_scan.get('endReason') == 'source_end'
            end_reason = reason or ('scanning' if running else source_scan.get('endReason') or 'unconfirmed_end')
            with self.lock:
                if self.closed:
                    return
                new, tokens = merge_scan(baseline, profile)
                new['revision'] = self.library['revision'] + 1
                new['scan'].update(running=running, seen=new['scan']['count'], complete=complete,
                                   coverage='streaming' if running else 'complete' if complete else 'partial',
                                   interrupted=bool(reason), endReason=end_reason)
                prior = read_json(self.directory / 'source-tokens.json', {})
                atomic(self.directory / 'source-tokens.json', {**prior, **tokens})
                atomic(self.directory / 'library.json', new)
                self.library, latest = new, profile

        def ingest_checkpoint():
            nonlocal checkpoint_stamp, checkpoint_content
            try:
                stat = checkpoint.stat()
            except FileNotFoundError:
                return
            if stat.st_mtime < self.scan_started or stat.st_mtime_ns == checkpoint_stamp:
                return
            profile = read_json(checkpoint, {})
            if not isinstance(profile.get('feeds'), list):
                return
            marker = profile.get('redbotScan') or {}
            content = digest(json.dumps({'feeds': profile['feeds'],
                'scan': {key: marker.get(key) for key in ('complete', 'endReason', 'seen')}},
                sort_keys=True, ensure_ascii=False))
            if content != checkpoint_content:
                publish(profile, True)
                checkpoint_content = content
            checkpoint_stamp = stat.st_mtime_ns

        def monitor():
            while not stop_monitor.wait(.25):
                try:
                    ingest_checkpoint()
                except (OSError, ValueError, Problem):
                    # The request finalizer performs a last read; a transient
                    # atomic replacement must not stop future batches.
                    continue

        with self.lock:
            self.library = {**self.library, 'revision': self.library['revision'] + 1,
                            'scan': {**self.library.get('scan', {}), 'at': iso(), 'running': True,
                                     'seen': 0, 'complete': False, 'coverage': 'streaming',
                                     'endReason': 'starting', 'interrupted': False}}
            atomic(self.directory / 'library.json', self.library)
        watcher = threading.Thread(target=monitor, daemon=True)
        watcher.start()
        failure = None
        profile = None
        try:
            out = self.backend.request('GET', '/api/v1/user/me?tab=fav')
            profile = out.get('data', out)
            if not isinstance(profile, dict) or not (isinstance(profile.get('feeds'), list) or
                    profile.get('feeds') is None and isinstance(profile.get('userBasicInfo'), dict)):
                profile = None
                raise Problem('scan_incomplete', 502)
        except Exception as error:
            failure = error
        finally:
            stop_monitor.set()
            watcher.join()
            ingest_checkpoint()
        if self.closed:
            return
        reason = 'cancelled' if self.scan_cancel.is_set() else 'source_unavailable' if failure else None
        if profile is not None and not reason:
            publish(profile, False)
        elif latest is not None:
            publish(latest, False, reason)
        else:
            with self.lock:
                self.library['scan'].update(running=False, complete=False, coverage='partial',
                                            interrupted=True, endReason=reason or 'source_unavailable')
                self.library['revision'] += 1
                atomic(self.directory / 'library.json', self.library)
            if failure:
                raise failure

    def cancel_scan(self):
        with self.lock:
            if not self.busy() or self.job['kind'] != 'scan':
                raise Problem('no_scan_running', 409)
            self.scan_cancel.set()
            self.job['cancelRequested'] = True
        # Stopping this isolated process cancels the browser request; credentials
        # and already-persisted saves remain available for a subsequent sync.
        self.backend.stop()
        return {'cancelRequested': True}

    def content_status(self, item, status, code=None):
        with self.lock:
            if self.closed:
                return
            item['contentReadStatus'] = status
            if status == 'running':
                item['contentReadAttemptedAt'] = iso()
            if code:
                item['contentReadError'] = {'code': code, 'at': iso(),
                                            'retainedPrevious': bool(item.get('contentReadAt'))}
            else:
                item.pop('contentReadError', None)
            self.library['revision'] += 1
            atomic(self.directory / 'library.json', self.library)

    def read(self, nid):
        if not ID.fullmatch(nid):
            raise Problem('save_not_found', 404)
        item = next((x for x in self.library['items'] if x['id'] == nid), None)
        if not item:
            raise Problem('save_not_found', 404)
        self.content_status(item, 'running')
        try:
            if self.state != 'connected':
                raise Problem('sign_in_required', 401)
            self.verify()
            if self.read_cancel.is_set():
                raise Problem('read_cancelled', 409)
            token = read_json(self.directory / 'source-tokens.json', {}).get(nid)
            if not token:
                raise Problem('sync_first', 409)
            out = self.backend.request('POST', '/api/v1/feeds/detail', {
                'feed_id': nid, 'xsec_token': token, 'load_all_comments': False})
            note = detail_note(out, nid)
            comments = detail_comments(out, note, nid)
            if comments is not None:
                with self.lock:
                    if not self.closed:
                        if self.read_cancel.is_set():
                            raise Problem('read_cancelled', 409)
                        item['comments'] = comments
                        self.library['revision'] += 1
                        atomic(self.directory / 'library.json', self.library)
            with self.lock:
                if self.closed:
                    return
                if self.read_cancel.is_set():
                    raise Problem('read_cancelled', 409)
                description = note['desc']
                item.update(description=description, hasContent=bool(description.strip() or (item.get('comments') or {}).get('items')),
                            contentReadAt=iso(), sourceMayHaveChanged=False,
                            coverage='post_text_only' if description.strip() else 'post_text_empty')
                if note.get('title'):
                    item['title'] = str(note['title'])
                if self.library.get('scan'):
                    self.library['scan']['readCount'] = sum(bool(x.get('description')) for x in self.library['items'])
                self.content_status(item, 'ready' if item['hasContent'] else 'empty')
        except Exception as error:
            code = 'read_cancelled' if self.read_cancel.is_set() else error.code if isinstance(error, Problem) else 'source_unavailable'
            self.content_status(item, 'cancelled' if code == 'read_cancelled' else 'failed', code)
            raise Problem(code, error.status if isinstance(error, Problem) else 502)

    def cancel_read(self):
        with self.lock:
            if not self.busy() or self.job['kind'] != 'read':
                raise Problem('no_read_running', 409)
            self.read_cancel.set()
            self.job['cancelRequested'] = True
        self.backend.stop()
        return {'cancelRequested': True}

    def read_video(self, nid):
        if not ID.fullmatch(nid):
            raise Problem('save_not_found', 404)
        item = next((x for x in self.library['items'] if x['id'] == nid), None)
        if not item:
            raise Problem('save_not_found', 404)
        if item.get('type') != 'video':
            raise Problem('not_video', 400)
        previous = item.get('videoAnalysis')
        self.content_status(item, 'running')
        try:
            if self.state != 'connected':
                raise Problem('sign_in_required', 401)
            self.verify()
            token = read_json(self.directory / 'source-tokens.json', {}).get(nid)
            if not token:
                raise Problem('sync_first', 409)
            out = self.backend.request('POST', '/api/v1/feeds/detail', {
                'feed_id':nid,'xsec_token':token,'load_all_comments':False})
            note = detail_note(out, nid)
            comments = detail_comments(out, note, nid)
            if comments is not None:
                with self.lock:
                    if not self.closed:
                        if self.video_cancel.is_set():
                            raise video.VideoError('video_cancelled')
                        item['comments'] = comments
                        self.library['revision'] += 1
                        atomic(self.directory / 'library.json', self.library)
            result = video.analyze(note, self.directory, self.video_cancel, previous)
            if self.video_cancel.is_set():
                raise video.VideoError('video_cancelled')
            if previous and previous.get('complete') and not result.get('complete'):
                raise video.VideoError('video_partial')
        except (Problem, video.VideoError, OSError, ValueError) as error:
            code = 'video_cancelled' if self.video_cancel.is_set() else error.code if isinstance(error, (Problem, video.VideoError)) else 'video_tool_failed'
            failure = {'code':code,'at':iso(),'retainedPrevious':bool(previous and previous.get('complete'))}
            result = {**previous, 'lastRefreshError':failure} if previous and previous.get('complete') else {
                'complete':False,'coverage':{'audio':'not_completed','frames':'not_completed','visual':'not_performed'},
                'error':code,'lastRefreshError':failure,'localCompute':True,'cloudCalls':0,'visualUnderstanding':False}
            with self.lock:
                if not self.closed:
                    item['videoAnalysis'] = result
                    self.library['revision'] += 1
                    atomic(self.directory / 'library.json', self.library)
            self.content_status(item, 'cancelled' if code == 'video_cancelled' else 'failed', code)
            raise Problem(code, error.status if isinstance(error, Problem) else 409)
        with self.lock:
            if self.closed:
                return
            result = {k:v for k,v in result.items() if k not in ('lastRefreshError','error')}
            item.update(videoAnalysis={**result,'readAt':iso()},description=note['desc'],
                        hasContent=bool(note['desc'].strip() or (item.get('comments') or {}).get('items') or result.get('transcript') or any(frame.get('text') for frame in result.get('frames', []))), contentReadAt=iso(),
                        coverage='video_audio_and_sampled_ocr' if result['complete'] else 'video_partial')
            self.library['revision'] += 1
            atomic(self.directory / 'library.json', self.library)
            self.content_status(item, 'ready' if item['hasContent'] else 'empty')

    def cancel_video(self):
        with self.lock:
            if not self.busy() or self.job['kind'] != 'video':
                raise Problem('no_video_running', 409)
            self.video_cancel.set()
            self.job['cancelRequested'] = True
        self.backend.stop()
        return {'cancelRequested':True}

    def close(self):
        with self.lock:
            self.closed = True
            self.video_cancel.set()
            self.read_cancel.set()
            self.scan_cancel.set()
            self.backend.disabled = True
            self.backend.stop()
            self.qr = None
            shutil.rmtree(self.directory, ignore_errors=True)


class Store:
    def __init__(self, root, binary, capacity=3, factory=MCP):
        self.root, self.binary, self.capacity, self.factory = root, binary, capacity, factory
        self.lock, self.sessions = threading.RLock(), {}
        root.mkdir(parents=True, exist_ok=True, mode=0o700)
        root.chmod(0o700)
        self.config = read_json(root / 'operator.json', {})
        if not self.config:
            self.config = {'invite': secrets.token_urlsafe(24)}
            atomic(root / 'operator.json', self.config)
        for p in root.glob('sessions/*/session.json'):
            meta = read_json(p, {})
            if meta.get('expires', 0) > time.time() and re.fullmatch('[a-f0-9]{32}', meta.get('id', '')):
                self.sessions[meta['tokenHash']] = Session(p.parent, meta, factory(binary, p.parent))
            else:
                shutil.rmtree(p.parent, ignore_errors=True)

    def create(self, invite, consent):
        if not isinstance(invite, str) or not hmac.compare_digest(invite, self.config['invite']):
            raise Problem('invite_required', 403)
        if consent is not True:
            raise Problem('consent_required', 400)
        with self.lock:
            self.reap()
            if len(self.sessions) >= self.capacity:
                raise Problem('beta_full', 429)
            sid, token = secrets.token_hex(16), secrets.token_urlsafe(32)
            meta = {'id': sid, 'tokenHash': digest(token), 'createdAt': iso(),
                    'expires': time.time() + TTL, 'pendingUntil': time.time() + PENDING_TTL}
            directory = self.root / 'sessions' / sid
            atomic(directory / 'session.json', meta)
            session = Session(directory, meta, self.factory(self.binary, directory))
            self.sessions[meta['tokenHash']] = session
            return {'token': token, 'sessionId': sid, 'expiresAt': session.expires_at()}

    def get(self, token):
        if not isinstance(token, str) or not re.fullmatch('[A-Za-z0-9_-]{40,100}', token):
            raise Problem('session_expired', 401)
        with self.lock:
            session = self.sessions.get(digest(token))
            if not session or session.closed or session.meta['expires'] < time.time():
                raise Problem('session_expired', 401)
            with session.lock:
                if session.abandoned():
                    session.close()
                    self.sessions.pop(digest(token), None)
                    raise Problem('session_expired', 401)
            return session

    def remove(self, token):
        with self.lock:
            session = self.get(token)
            session.close()
            self.sessions.pop(digest(token), None)

    def reap(self):
        with self.lock:
            for key, session in list(self.sessions.items()):
                with session.lock:
                    if session.meta['expires'] < time.time() or session.abandoned():
                        session.close()
                        del self.sessions[key]

    def stop(self):
        for session in self.sessions.values():
            session.video_cancel.set()
            session.scan_cancel.set()
            session.backend.stop()
        for session in self.sessions.values():
            worker = getattr(session, 'worker', None)
            if worker:
                worker.join(timeout=12)


def static_asset(path):
    name = 'index.html' if path == '/' else unquote(path).lstrip('/')
    parts = Path(name).parts
    if not parts or any(p.startswith('.') for p in parts) or ('/' in name and not name.startswith('vendor/')):
        raise Problem('not_found', 404)
    target = (APP / name).resolve()
    if not target.is_relative_to(APP.resolve()) or not target.is_file():
        raise Problem('not_found', 404)
    if target.suffix.lower() not in ('.html', '.js', '.mjs', '.css', '.json', '.webmanifest', '.wasm', '.png', '.svg', '.ico', '.woff', '.woff2'):
        raise Problem('not_found', 404)
    import mimetypes
    mime = {'.mjs':'text/javascript', '.js':'text/javascript', '.webmanifest':'application/manifest+json', '.wasm':'application/wasm'}.get(target.suffix.lower()) or mimetypes.guess_type(str(target))[0] or 'application/octet-stream'
    if mime.startswith('text/') or mime == 'application/json': mime += '; charset=utf-8'
    return target.read_bytes(), mime


def make_handler(store, origins, host):
    class Handler(BaseHTTPRequestHandler):
        server_version = 'RedBot'

        def setup(self):
            super().setup()
            self.connection.settimeout(15)

        def log_message(self, *_):
            pass

        def send(self, data, code=200, mime='application/json'):
            body = json.dumps(data, ensure_ascii=False).encode() if mime == 'application/json' else data
            self.send_response(code)
            self.send_header('Content-Type', mime)
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Referrer-Policy', 'no-referrer')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('X-Frame-Options', 'DENY')
            origin = self.headers.get('Origin')
            if origin in origins:
                self.send_header('Access-Control-Allow-Origin', origin)
                self.send_header('Vary', 'Origin')
                self.send_header('Access-Control-Allow-Headers', 'Authorization, Content-Type')
                self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            try:
                self.wfile.write(body)
            except (BrokenPipeError, ConnectionResetError):
                pass

        def allowed(self):
            # A reverse proxy must use --http-host-header with this loopback host.
            if self.headers.get('Host') != host:
                raise Problem('wrong_host', 403)
            origin = self.headers.get('Origin')
            if origin is not None and origin not in origins:
                raise Problem('wrong_origin', 403)

        def do_OPTIONS(self):
            try:
                self.allowed()
                self.send({})
            except Problem as e:
                self.send({'error': e.code}, e.status)

        def do_GET(self):
            self.handle_request('GET')

        def do_POST(self):
            self.handle_request('POST')

        def handle_request(self, method):
            try:
                self.allowed()
                path = self.path.split('?', 1)[0]
                if method == 'GET' and path == '/api/capabilities':
                    return self.send({'redbotConnector': 1, 'readOnly': True, 'inviteRequired': True,
                                      'automatic': 'while_app_open', 'retentionDays': 7, 'llmCalls': False, 'cloudInferenceCalls': False,
                                      'video': {'onDemand': True, 'localModelInference': True, 'audio': 'whisper_asr',
                                                'frames': 'sampled_ocr', 'visualUnderstanding': False, 'maxConcurrent': 1}})
                if method == 'GET' and not path.startswith('/api/'):
                    content, mime = static_asset(path)
                    return self.send(content, mime=mime)
                body = {}
                if method == 'POST':
                    if self.headers.get('Content-Type', '').split(';')[0] != 'application/json':
                        raise Problem('invalid_request', 400)
                    size = int(self.headers.get('Content-Length', '0'))
                    if not 0 < size <= 16000:
                        raise Problem('invalid_request', 400)
                    body = json.loads(self.rfile.read(size))
                    if not isinstance(body, dict):
                        raise Problem('invalid_request', 400)
                if method == 'POST' and path == '/api/session':
                    return self.send(store.create(body.get('invite'), body.get('consent')))
                token = self.headers.get('Authorization', '').removeprefix('Bearer ')
                session = store.get(token)
                if method == 'GET' and path == '/api/connection':
                    return self.send(session.status())
                if method == 'GET' and path == '/api/library':
                    with session.lock:
                        return self.send(session.library)
                if method == 'POST' and path == '/api/connect':
                    return self.send(session.start('connect', session.connect))
                if method == 'POST' and path == '/api/verify':
                    return self.send(session.start('verify', session.verify))
                if method == 'POST' and path == '/api/sync':
                    scan = session.library.get('scan', {})
                    if scan.get('at') and time.time() - calendar.timegm(time.strptime(scan['at'], '%Y-%m-%dT%H:%M:%SZ')) < 60:
                        raise Problem('scan_cooldown', 429)
                    return self.send(session.start('scan', session.scan))
                if method == 'POST' and path == '/api/cancel-sync':
                    return self.send(session.cancel_scan())
                if method == 'POST' and path == '/api/cancel-video':
                    return self.send(session.cancel_video())
                if method == 'POST' and path == '/api/video':
                    nid = body.get('id', '')
                    if not isinstance(nid, str):
                        raise Problem('invalid_request', 400)
                    return self.send(session.start('video', lambda: session.read_video(nid), nid))
                if method == 'POST' and path == '/api/cancel-read':
                    return self.send(session.cancel_read())
                if method == 'POST' and path == '/api/read':
                    nid = body.get('id', '')
                    if not isinstance(nid, str):
                        raise Problem('invalid_request', 400)
                    return self.send(session.start('read', lambda: session.read(nid), nid))
                if method == 'POST' and path == '/api/disconnect':
                    store.remove(token)
                    return self.send({'disconnected': True, 'serverDataDeleted': True})
                raise Problem('not_found', 404)
            except Problem as e:
                self.send({'error': e.code}, e.status)
            except (ValueError, TypeError, KeyError):
                self.send({'error': 'invalid_request'}, 400)
            except Exception:
                self.send({'error': 'service_unavailable'}, 500)
    return Handler


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--binary', type=Path, required=True)
    parser.add_argument('--data-dir', type=Path, required=True)
    parser.add_argument('--port', type=int, default=8776)
    parser.add_argument('--capacity', type=int, default=3)
    parser.add_argument('--origin', action='append', default=['https://sidecourt.space'])
    args = parser.parse_args()
    os.umask(0o077)
    runtime = read_json(Path(__file__).with_name('video-runtime.local.json'), {})
    for key in ('REDBOT_FFMPEG', 'REDBOT_WHISPER', 'REDBOT_WHISPER_MODEL', 'REDBOT_WHISPER_SHA256', 'REDBOT_OCR'):
        if isinstance(runtime.get(key), str):
            os.environ.setdefault(key, runtime[key])
    store = Store(args.data_dir.resolve(), args.binary.resolve(), args.capacity)
    host = f'127.0.0.1:{args.port}'
    origins = set(args.origin + ['http://' + host])
    server = ThreadingHTTPServer(('127.0.0.1', args.port), make_handler(store, origins, host))
    server.daemon_threads = True
    print('RedBot account connector ready on ' + host + '. Invite kept in operator.json.', flush=True)
    def reap():
        while True:
            time.sleep(60)
            store.reap()
    threading.Thread(target=reap, daemon=True).start()
    def shutdown_signal(*_):
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, shutdown_signal)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        store.stop()


if __name__ == '__main__':
    main()
