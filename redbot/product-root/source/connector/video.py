"""Bounded local video reading. No cookies or cloud model calls."""
import hashlib
import http.client
import ipaddress
import json
import os
import platform
from pathlib import Path
import socket
import ssl
import subprocess
import tempfile
import time
from urllib.parse import urlsplit, urljoin

MAX_BYTES = 100 * 1024 * 1024
MAX_SECONDS = 600
PIPELINE = 'whisper-cpp-1.9.2-tiny+apple-vision-v1-macos-' + platform.mac_ver()[0]

class VideoError(Exception):
    def __init__(self, code):
        self.code = code
        super().__init__(code)

def check(cancel, deadline):
    if cancel.is_set(): raise VideoError('video_cancelled')
    if time.monotonic() > deadline: raise VideoError('video_timeout')

def normalize_source_url(url):
    # Some normal page media records use HTTP CDN URLs. Upgrade only this known
    # host family; credentials, odd ports and non-CDN hosts remain rejected.
    p = urlsplit(url)
    host = p.hostname or ''
    if p.scheme == 'http':
        if p.username or p.password or p.port not in (None, 80) or not (host.endswith('.xhscdn.com') or host.endswith('.xiaohongshu.com')):
            raise VideoError('video_url_not_allowed')
        return p._replace(scheme='https', netloc=host).geturl()
    return url


def resolve(url):
    p = urlsplit(url)
    host = p.hostname or ''
    if p.scheme != 'https' or p.username or p.password or p.port not in (None, 443) or not (host.endswith('.xhscdn.com') or host.endswith('.xiaohongshu.com')):
        raise VideoError('video_url_not_allowed')
    addresses = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
    if not addresses or any(not ipaddress.ip_address(a[4][0]).is_global for a in addresses):
        raise VideoError('video_url_not_allowed')
    return p, addresses[0][4][0]

class PinnedHTTPS(http.client.HTTPSConnection):
    def __init__(self, host, address):
        super().__init__(host, timeout=10, context=ssl.create_default_context())
        self.address = address
    def connect(self):
        sock = socket.create_connection((self.address, 443), self.timeout)
        self.sock = self._context.wrap_socket(sock, server_hostname=self.host)

def download(url, path, cancel, deadline):
    # Validate every redirect and pin the validated public address to avoid DNS rebinding.
    for _ in range(4):
        check(cancel, deadline)
        p, address = resolve(url)
        conn = PinnedHTTPS(p.hostname, address)
        try:
            conn.request('GET', p.path + ('?' + p.query if p.query else ''), headers={'User-Agent':'RedBot/1.0'})
            response = conn.getresponse()
            if response.status in (301,302,303,307,308):
                url = urljoin(url, response.getheader('Location', ''))
                continue
            if response.status != 200: raise VideoError('video_download_failed')
            if int(response.getheader('Content-Length', '0')) > MAX_BYTES: raise VideoError('video_too_large')
            size = 0
            with open(path, 'wb') as f:
                while True:
                    check(cancel, deadline)
                    chunk = response.read(65536)
                    if not chunk: break
                    size += len(chunk)
                    if size > MAX_BYTES: raise VideoError('video_too_large')
                    f.write(chunk)
            return
        finally: conn.close()
    raise VideoError('video_redirect_limit')

def command(args, cancel, deadline):
    with tempfile.TemporaryFile() as output, tempfile.TemporaryFile() as errors:
        try:
            proc = subprocess.Popen([str(a) for a in args], stdout=output, stderr=errors,
                                    start_new_session=True)
        except OSError:
            raise VideoError('video_tool_failed')
        try:
            while proc.poll() is None:
                check(cancel, deadline)
                time.sleep(.1)
            if proc.returncode: raise VideoError('video_tool_failed')
            output.seek(0)
            return output.read(2_000_000).decode('utf-8')
        finally:
            if proc.poll() is None:
                import signal
                try: os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError: pass
                proc.wait()

def tools():
    ffmpeg = os.environ.get('REDBOT_FFMPEG')
    model = os.environ.get('REDBOT_WHISPER_MODEL')
    whisper = os.environ.get('REDBOT_WHISPER', '/opt/homebrew/Cellar/whisper-cpp/1.9.2/bin/whisper-cli')
    ocr = os.environ.get('REDBOT_OCR')
    if not ffmpeg or not model or not all(Path(x).is_file() for x in (ffmpeg, model, whisper)):
        raise VideoError('video_setup_required')
    # Operator pins the actual model bytes, never an auto-updated model alias.
    expected = os.environ.get('REDBOT_WHISPER_SHA256', '')
    if expected != 'be07e048e1e599ad46341c8d2a135645097a538221678b7acdd1b1919c6e1b21' or hashlib.sha256(Path(model).read_bytes()).hexdigest() != expected:
        raise VideoError('video_model_mismatch')
    return ffmpeg, whisper, model, ocr

def select_source(note):
    video = note.get('video') or {}
    media = video.get('media') or {}
    meta = media.get('video') or {}
    if meta.get('drmType'): raise VideoError('video_protected')
    choices = [s for s in (media.get('stream') or {}).get('h264', []) if s.get('masterUrl') and s.get('format', 'mp4') == 'mp4']
    if not choices: raise VideoError('video_source_unavailable')
    choices.sort(key=lambda s: s.get('size') or 10**12)
    s = choices[0]
    duration = s.get('duration', 0) / 1000 or meta.get('duration') or video.get('capa', {}).get('duration')
    if not duration or duration > MAX_SECONDS: raise VideoError('video_duration_limit')
    if s.get('size', 0) > MAX_BYTES: raise VideoError('video_too_large')
    identity = {'mediaPath':urlsplit(s['masterUrl']).path, 'mediaId':media.get('videoId'), 'md5':meta.get('md5'), 'duration':duration,
                'stream':{k:s.get(k) for k in ('width','height','size','videoCodec','qualityType')},
                'noteTime':note.get('time'), 'desc':note.get('desc'), 'pipeline':PIPELINE}
    identity['modelSHA256'] = os.environ.get('REDBOT_WHISPER_SHA256')
    version = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()
    return normalize_source_url(s['masterUrl']), duration, version

def analyze_file(path, duration, cancel, deadline):
    ffmpeg, whisper, model, ocr = tools()
    result = {'pipeline':PIPELINE, 'durationSeconds':duration, 'localCompute':True,
              'cloudCalls':0, 'visualUnderstanding':False, 'transcript':[], 'frames':[],
              'coverage':{'audio':'pending','frames':'pending','visual':'not_performed'}}
    progress = command([ffmpeg,'-v','error','-nostdin','-protocol_whitelist','file,pipe','-f','mov','-i',path,
                        '-t',MAX_SECONDS+1,'-progress','pipe:1','-f','null','-'],cancel,deadline)
    actual = max([int(line.split('=')[1])/1000000 for line in progress.splitlines() if line.startswith('out_time_us=') and line.split('=')[1].isdigit()] or [0])
    if actual > MAX_SECONDS or actual <= 0: raise VideoError('video_duration_limit')
    duration = actual
    result['durationSeconds'] = actual
    with tempfile.TemporaryDirectory(prefix='redbot-analysis-') as folder:
        temp = Path(folder)
        try:
            command([ffmpeg,'-v','error','-nostdin','-protocol_whitelist','file,pipe','-f','mov','-i',path,'-t',MAX_SECONDS,'-vn','-ar','16000','-ac','1',temp/'audio.wav'], cancel, deadline)
            command([whisper,'-m',model,'-f',temp/'audio.wav','-l','auto','-oj','-of',temp/'speech'], cancel, deadline)
            data = json.loads((temp/'speech.json').read_text())
            result['transcript'] = [{'start':r['offsets']['from']/1000,'end':r['offsets']['to']/1000,'text':r['text'].strip()} for r in data.get('transcription', [])][:4000]
            result['coverage']['audio'] = 'transcribed' if result['transcript'] else 'no_speech_detected'
        except VideoError as e:
            if e.code in ('video_cancelled','video_timeout'): raise
            result['coverage']['audio'] = e.code
        # Uniform bounded samples, explicitly not all frames or semantic scene analysis.
        interval = max(2, duration / 12)
        try:
            command([ffmpeg,'-v','error','-nostdin','-protocol_whitelist','file,pipe','-f','mov','-i',path,'-t',MAX_SECONDS,'-vf',f'fps=1/{interval},scale=960:-2','-frames:v','12',temp/'frame-%02d.png'], cancel, deadline)
            for i, frame in enumerate(sorted(temp.glob('frame-*.png'))):
                text = json.loads(command([ocr,frame],cancel,deadline)) if ocr and Path(ocr).is_file() else None
                if text is not None:
                    text = [{'text':str(row.get('text','')), 'confidence':max(0.0,min(1.0,float(row.get('confidence',0))))} for row in text]
                result['frames'].append({'at':round((i+.5)*interval,2),'text':text})
            result['coverage']['frames'] = 'sampled_ocr' if ocr and result['frames'] else 'ocr_setup_required'
            result['sampling'] = {'method':'uniform','intervalSeconds':interval,'maxFrames':12,'allFrames':False}
        except VideoError as e:
            if e.code in ('video_cancelled','video_timeout'): raise
            result['coverage']['frames'] = e.code
    result['complete'] = result['coverage']['audio'] in ('transcribed','no_speech_detected') and result['coverage']['frames'] == 'sampled_ocr'
    return result

def analyze(note, directory, cancel, previous=None):
    url, duration, version = select_source(note)
    # Cache account-local, content-version bound; signed URLs never persist.
    if previous and previous.get('sourceVersion') == version and previous.get('complete'):
        return {**previous,'cached':True}
    tools() # fail before any media request if local runtime is missing
    deadline = time.monotonic() + 900
    with tempfile.TemporaryDirectory(prefix='video-', dir=directory) as folder:
        path = Path(folder)/'source.mp4'
        download(url,path,cancel,deadline)
        result = analyze_file(path,duration,cancel,deadline)
    return {**result,'sourceVersion':version,'cached':False}
