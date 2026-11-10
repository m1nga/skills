#!/usr/bin/env python3
"""Replay a synthetic saved-research update through the bundled comparator."""

import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory


COMPARATOR = Path(__file__).resolve().parents[1] / "scripts" / "source_delta.py"
SCOPE = "onboarding-research"
REVIEWED = {
    "note-01": "Keep the first task visible on the setup screen.",
    "note-02": "Recovery originally started the form over.",
}
SOURCES = {
    "notes/note-02-v2.txt": "Let people retry without clearing answers already entered.",
    "notes/note-41-v1.txt": "Show what will happen before asking for access.",
}
EXPECTED = {
    "reused_review": REVIEWED["note-01"],
    "new_evidence": [SOURCES["notes/note-41-v1.txt"], SOURCES["notes/note-02-v2.txt"]],
    "unread": "note-03",
    "unresolved_absence": "note-40",
}


def record(number, revision=1):
    item_id = f"note-{number:02}"
    return {"id": item_id, "revision": f"v{revision}", "ref": f"notes/{item_id}-v{revision}.txt"}


def write_snapshot(path, coverage, records):
    path.write_text(
        json.dumps({"scope": SCOPE, "coverage": coverage, "records": records}, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


def compare_pages(previous, current):
    offset = 0
    while offset is not None:
        raw = subprocess.check_output(
            [sys.executable, str(COMPARATOR), str(previous), str(current), "--limit", "2", "--offset", str(offset)]
        )
        yield raw
        offset = json.loads(raw)["next_offset"]


def full_scan_result(previous, current):
    before, after = (json.loads(path.read_bytes()) for path in (previous, current))
    old, new = ({item["id"]: item for item in snapshot["records"]} for snapshot in (before, after))
    return {
        "reused_review": REVIEWED["note-01"] if old["note-01"] == new["note-01"] else None,
        "new_evidence": [SOURCES[new[key]["ref"]] for key in ("note-41", "note-02") if new[key] != old.get(key)],
        "unread": "note-03" if "note-03" in new and "note-03" not in REVIEWED else None,
        "unresolved_absence": "note-40" if "note-40" not in new and after["coverage"] == "partial" else None,
    }


def delta_result(pages):
    first = pages[0]
    changes = [row for page in pages for row in page["records"]]
    seen_changes = {row["id"] for row in changes}
    return {
        "reused_review": REVIEWED["note-01"] if "note-01" not in seen_changes else None,
        "new_evidence": [SOURCES[row["ref"]] for row in changes if row["status"] in ("added", "changed")],
        "unread": "note-03" if "note-03" not in seen_changes and "note-03" not in REVIEWED else None,
        "unresolved_absence": next(
            (row["id"] for row in changes if row["status"] == "not_seen" and first["current_coverage"] == "partial"),
            None,
        ),
    }


def main():
    with TemporaryDirectory() as directory:
        previous = Path(directory) / "previous.json"
        current = Path(directory) / "current.json"
        write_snapshot(previous, "complete", [record(number) for number in range(1, 41)])
        current_records = [record(number, 2 if number == 2 else 1) for number in range(1, 40)]
        write_snapshot(current, "partial", current_records + [record(41)])
        payloads = list(compare_pages(previous, current))
        pages = [json.loads(payload) for payload in payloads]
        baseline = full_scan_result(previous, current)
        optimized = delta_result(pages)
        if baseline != EXPECTED or optimized != baseline:
            raise SystemExit(f"Outcome mismatch: full={baseline!r}, delta={optimized!r}")

        print(json.dumps({
            "input": "synthetic saved research",
            "coverage": {"previous": pages[0]["previous_coverage"], "current": pages[0]["current_coverage"]},
            "counts": pages[0]["counts"],
            "page_count": len(pages),
            "metadata_payload_bytes": {
                "full_manifests": previous.stat().st_size + current.stat().st_size,
                "all_delta_pages": sum(map(len, payloads)),
            },
            "provider_tokens": "not measured",
            "same_expected_outcome": True,
            "outcome": optimized,
        }, indent=2))


if __name__ == "__main__":
    main()
