"""Explicit project-local setup; no service restart or global configuration."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import urllib.request
ROOT = Path(__file__).resolve().parents[1]
MODEL_SHA = 'be07e048e1e599ad46341c8d2a135645097a538221678b7acdd1b1919c6e1b21'
REVISION = '5359861c739e955e79d9a303bcbc70fb988958b1'
venv = ROOT/'.video-venv'
subprocess.run([sys.executable,'-m','venv',venv],check=True)
subprocess.run([venv/'bin/python','-m','pip','install','imageio-ffmpeg==0.6.0'],check=True)
model = ROOT/'connector/video-models/ggml-tiny.bin'
model.parent.mkdir(parents=True,exist_ok=True)
if not model.is_file() or hashlib.sha256(model.read_bytes()).hexdigest()!=MODEL_SHA:
    temp = model.with_suffix('.download')
    try:
        with urllib.request.urlopen(f'https://huggingface.co/ggerganov/whisper.cpp/resolve/{REVISION}/ggml-tiny.bin',timeout=30) as r,temp.open('wb') as f:
            size=0
            while True:
                b=r.read(1024*1024)
                if not b:break
                size+=len(b)
                if size>80_000_000:raise RuntimeError('model_size_mismatch')
                f.write(b)
        if hashlib.sha256(temp.read_bytes()).hexdigest()!=MODEL_SHA:raise RuntimeError('model_checksum_mismatch')
        temp.replace(model)
    finally:temp.unlink(missing_ok=True)
ocr=venv/'bin/redbot-ocr'
subprocess.run(['/usr/bin/swiftc',ROOT/'connector/video_ocr.swift','-o',ocr],check=True)
ffmpeg=subprocess.check_output([venv/'bin/python','-c','import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())'],text=True).strip()
config={'REDBOT_FFMPEG':ffmpeg,'REDBOT_WHISPER':'/opt/homebrew/Cellar/whisper-cpp/1.9.2/bin/whisper-cli','REDBOT_WHISPER_MODEL':str(model),'REDBOT_WHISPER_SHA256':MODEL_SHA,'REDBOT_OCR':str(ocr)}
(ROOT/'connector/video-runtime.local.json').write_text(json.dumps(config,indent=2))
print('Local video runtime prepared. Configure the next explicit service start with video-runtime.local.json.')
