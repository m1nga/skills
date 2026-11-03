"""RedBot's invite-only account connector. No model, owner session, or write tool.

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
from urllib.request import Request, urlopen

APP = Path(__file__).resolve().parents[1] / 'app'
ID = re.compile(r'^[a-f0-9]{24}$')
TTL = 7 * 86400


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
                 'complete': False, 'coverage': 'bounded',
                 'llmTokens': 0, 'readCount': sum(bool(x.get('description')) for x in result),
                 'analyzedCount': 0},
    }, tokens


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
                with urlopen(f'http://127.0.0.1:{self.port}/health', timeout=0.3) as response:
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
                with urlopen(req, timeout=190) as response:
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
        self.library = read_json(directory / 'library.json', {'version': 1, 'items': []})

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
            checkpoint = self.directory / 'scan-checkpoint.json'
            if self.busy() and self.job['kind'] == 'scan' and self.scan_started and checkpoint.exists() and checkpoint.stat().st_mtime >= self.scan_started:
                partial = read_json(checkpoint, {})
                progress = {'seen': len(partial.get('feeds') or []), 'complete': False}
            return {'state': self.state, 'nickname': self.meta.get('nickname', ''),
                    'sessionId': self.meta['id'], 'expiresAt': self.meta['expires'],
                    'qr': self.qr if self.state == 'waiting' else None,
                    'qrExpiresAt': self.qr_expires, 'job': self.job,
                    'scan': self.library.get('scan'), 'progress': progress, 'items': len(self.library['items'])}

    def busy(self):
        return bool(self.job and self.job['state'] == 'running')

    def start(self, kind, fn):
        with self.lock:
            if self.closed:
                raise Problem('session_expired', 401)
            if self.busy():
                raise Problem('busy', 409)
            job_id = secrets.token_hex(10)
            self.job = {'id': job_id, 'kind': kind, 'state': 'running', 'startedAt': iso()}

        def run():
            try:
                fn()
                with self.lock:
                    if self.closed:
                        return
                    self.job = {**self.job, 'state': 'done', 'finishedAt': iso()}
                if kind == 'verify' and self.state == 'connected':
                    self.start('scan', self.scan)
            except Exception as e:
                with self.lock:
                    if not self.closed:
                        self.job = {**self.job, 'state': 'failed', 'error': e.code if isinstance(e, Problem) else 'source_unavailable'}
        threading.Thread(target=run, daemon=True).start()
        return {'jobId': job_id}

    def connect(self):
        if self.closed:
            raise Problem('session_expired', 401)
        if self.state == 'connected':
            raise Problem('already_connected', 409)
        self.qr = None
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
            self.meta.update(account=account, nickname=str(out.get('username', ''))[:120])
            atomic(self.directory / 'session.json', self.meta)
            self.state, self.qr = 'connected', None

    def scan(self):
        if self.state != 'connected':
            raise Problem('sign_in_required', 401)
        # Check identity on every scan, including after a service restart.
        self.verify()
        self.scan_started = time.time()
        interrupted = False
        try:
            out = self.backend.request('GET', '/api/v1/user/me?tab=fav')
            profile = out.get('data', out)
        except Problem:
            # Recover only a checkpoint made by THIS account's CURRENT scan.
            checkpoint = self.directory / 'scan-checkpoint.json'
            if not checkpoint.exists() or checkpoint.stat().st_mtime < self.scan_started:
                raise
            profile = read_json(checkpoint, {})
            if not profile.get('feeds'):
                raise
            interrupted = True
        if profile.get('feeds') is None and isinstance(profile.get('userBasicInfo'), dict):
            profile['feeds'] = []
        if not isinstance(profile.get('feeds'), list):
            raise Problem('scan_incomplete', 502)
        with self.lock:
            if self.closed:
                return
            new, tokens = merge_scan(self.library, profile)
            new['scan']['interrupted'] = interrupted
            prior = read_json(self.directory / 'source-tokens.json', {})
            atomic(self.directory / 'source-tokens.json', {**prior, **tokens})
            atomic(self.directory / 'library.json', new)
            self.library = new

    def read(self, nid):
        if self.state != 'connected':
            raise Problem('sign_in_required', 401)
        if not ID.fullmatch(nid) or not any(x['id'] == nid for x in self.library['items']):
            raise Problem('save_not_found', 404)
        self.verify()
        token = read_json(self.directory / 'source-tokens.json', {}).get(nid)
        if not token:
            raise Problem('sync_first', 409)
        out = self.backend.request('POST', '/api/v1/feeds/detail', {
            'feed_id': nid, 'xsec_token': token, 'load_all_comments': False})
        content = out.get('data', out)
        note = content.get('note') or content.get('data', {}).get('note')
        if not isinstance(note, dict):
            raise Problem('source_unavailable', 502)
        with self.lock:
            if self.closed:
                return
            item = next(x for x in self.library['items'] if x['id'] == nid)
            item.update(description=str(note.get('desc', '')), hasContent=bool(note.get('desc')),
                        contentReadAt=iso(), sourceMayHaveChanged=False,
                        coverage='post_text_only')
            if note.get('title'):
                item['title'] = str(note['title'])
            # We deliberately do not copy comment identities, signed media,
            # session tokens, or an invented video transcript into the library.
            if self.library.get('scan'):
                self.library['scan']['readCount'] = sum(bool(x.get('description')) for x in self.library['items'])
            atomic(self.directory / 'library.json', self.library)

    def close(self):
        with self.lock:
            self.closed = True
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
            meta = {'id': sid, 'tokenHash': digest(token), 'createdAt': iso(), 'expires': time.time() + TTL}
            directory = self.root / 'sessions' / sid
            atomic(directory / 'session.json', meta)
            session = Session(directory, meta, self.factory(self.binary, directory))
            self.sessions[meta['tokenHash']] = session
            return {'token': token, 'sessionId': sid, 'expiresAt': meta['expires']}

    def get(self, token):
        if not isinstance(token, str) or not re.fullmatch('[A-Za-z0-9_-]{40,100}', token):
            raise Problem('session_expired', 401)
        with self.lock:
            session = self.sessions.get(digest(token))
            if not session or session.closed or session.meta['expires'] < time.time():
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
                if session.meta['expires'] < time.time():
                    session.close()
                    del self.sessions[key]

    def stop(self):
        for session in self.sessions.values():
            session.backend.stop()


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
                                      'automatic': 'while_app_open', 'retentionDays': 7, 'llmCalls': False})
                if method == 'GET' and not path.startswith('/api/'):
                    filename = 'index.html' if path == '/' else path[1:]
                    if '/' in filename or filename.startswith('.') or not (APP / filename).is_file():
                        raise Problem('not_found', 404)
                    import mimetypes
                    return self.send((APP / filename).read_bytes(), mime=(mimetypes.guess_type(filename)[0] or 'application/octet-stream') + '; charset=utf-8')
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
                if method == 'POST' and path == '/api/sync':
                    scan = session.library.get('scan', {})
                    if scan.get('at') and time.time() - calendar.timegm(time.strptime(scan['at'], '%Y-%m-%dT%H:%M:%SZ')) < 60:
                        raise Problem('scan_cooldown', 429)
                    return self.send(session.start('scan', session.scan))
                if method == 'POST' and path == '/api/read':
                    nid = body.get('id', '')
                    if not isinstance(nid, str):
                        raise Problem('invalid_request', 400)
                    return self.send(session.start('read', lambda: session.read(nid)))
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
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        store.stop()


if __name__ == '__main__':
    main()
