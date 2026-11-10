#!/usr/bin/env python3
"""Prepare the pinned browser WASM asset without executing it."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile
import time
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
ASSET = "ort-wasm-simd-threaded.jsep.wasm"
VENDOR = ROOT / "app" / "vendor" / "transformers"
SOURCE = (
    "https://raw.githubusercontent.com/m1nga/skills/"
    "278e12261fd7f4fefc2a632138665510ccbcad6e/"
    "redbot/product-root/source/app/vendor/transformers/" + ASSET
)
SOCKET_TIMEOUT = 15
DOWNLOAD_SECONDS = 120


def matches(path, expected):
    if path.stat().st_size != expected["bytes"]:
        return False
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest() == expected["sha256"]


def prepare(target, expected, repair=False, opener=None):
    """Download to a sibling temporary file, verify, then atomically replace."""
    target = Path(target)
    if target.exists() and not repair:
        if matches(target, expected):
            return "already verified; skipped download"
        raise ValueError("Existing WASM failed verification; rerun with --repair")
    opener = opener or urllib.request.urlopen
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        deadline = time.monotonic() + DOWNLOAD_SECONDS
        with tempfile.NamedTemporaryFile(
            dir=target.parent, prefix="." + target.name + ".", suffix=".tmp", delete=False
        ) as output:
            temporary = Path(output.name)
            # urllib's default HTTPS context verifies certificates and hostnames.
            with opener(SOURCE, timeout=SOCKET_TIMEOUT) as response:
                received = 0
                while True:
                    if time.monotonic() >= deadline:
                        raise TimeoutError("WASM download exceeded its time limit")
                    # A single buffered read avoids waiting for a full chunk
                    # while a server trickles bytes past the total deadline.
                    chunk = response.read1(64 * 1024)
                    if not chunk:
                        break
                    received += len(chunk)
                    if received > expected["bytes"]:
                        raise ValueError("Downloaded WASM exceeds the pinned byte count")
                    output.write(chunk)
            output.flush()
            os.fsync(output.fileno())
        if not matches(temporary, expected):
            raise ValueError("Downloaded WASM does not match the pinned size and SHA256")
        os.replace(temporary, target)
        return "downloaded and verified"
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repair", action="store_true", help="redownload and verify before replacing")
    args = parser.parse_args()
    try:
        expected = json.loads((VENDOR / "assets.lock.json").read_text())[ASSET]
        result = prepare(VENDOR / ASSET, expected, repair=args.repair)
    except (OSError, ValueError, TimeoutError) as exc:
        parser.exit(1, f"Runtime preparation failed: {exc}\n")
    print(f"{ASSET}: {result}")


if __name__ == "__main__":
    main()
