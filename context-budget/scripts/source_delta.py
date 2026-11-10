#!/usr/bin/env python3
"""Compare two explicit source manifests and return a bounded page of changes."""
import argparse
import json
from pathlib import Path
import sys

COVERAGES = {"complete", "partial", "unknown"}


def read_manifest(path):
    document = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise ValueError(f"{path.name}: expected a manifest object")
    scope = document.get("scope")
    coverage = document.get("coverage")
    rows = document.get("records")
    if not isinstance(scope, str) or not scope.strip() or len(scope) > 200:
        raise ValueError(f"{path.name}: scope must be a nonempty string up to 200 characters")
    if not isinstance(coverage, str) or coverage not in COVERAGES:
        raise ValueError(f"{path.name}: coverage must be complete, partial or unknown")
    if not isinstance(rows, list):
        raise ValueError(f"{path.name}: records must be a list")

    records = {}
    duplicates = 0
    for number, row in enumerate(rows, start=1):
        if not isinstance(row, dict) or set(row) != {"id", "revision", "ref"}:
            raise ValueError(f"{path.name}: record {number} needs exactly id, revision and ref")
        for field, maximum in (("id", 200), ("revision", 200), ("ref", 1200)):
            value = row[field]
            if not isinstance(value, str) or not value.strip() or len(value) > maximum:
                raise ValueError(f"{path.name}: invalid {field} in record {number}")
        key = row["id"]
        if key in records:
            if records[key] != row:
                raise ValueError(f"{path.name}: conflicting duplicate ID at record {number}")
            duplicates += 1
        else:
            records[key] = row
    return scope, coverage, records, duplicates


def compare(previous, current, offset, limit):
    old_scope, old_coverage, old, old_duplicates = previous
    scope, coverage, new, new_duplicates = current
    if scope != old_scope:
        raise ValueError("snapshot scopes differ; compare the same source and selection")

    added = sorted(new.keys() - old.keys())
    changed = sorted(key for key in new.keys() & old.keys() if new[key] != old[key])
    not_seen = sorted(old.keys() - new.keys())
    differences = (
        [dict(status="added", **new[key]) for key in added]
        + [dict(status="changed", **new[key]) for key in changed]
        + [dict(status="not_seen", **old[key]) for key in not_seen]
    )
    total = len(differences)
    if offset > total:
        raise ValueError(f"offset {offset} is beyond {total} differences")
    return {
        "scope": scope,
        "previous_coverage": old_coverage,
        "current_coverage": coverage,
        "counts": {
            "previous_unique": len(old),
            "current_unique": len(new),
            "added": len(added),
            "changed": len(changed),
            "not_seen": len(not_seen),
            "unchanged": len(new) - len(added) - len(changed),
            "previous_duplicate_copies": old_duplicates,
            "current_duplicate_copies": new_duplicates,
        },
        "offset": offset,
        "next_offset": offset + limit if offset + limit < total else None,
        "records": differences[offset:offset + limit],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("previous", type=Path)
    parser.add_argument("current", type=Path)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()
    if args.offset < 0 or not 1 <= args.limit <= 100:
        parser.error("offset must be nonnegative and limit must be between 1 and 100")
    try:
        result = compare(
            read_manifest(args.previous), read_manifest(args.current), args.offset, args.limit
        )
    except (OSError, UnicodeError, ValueError) as error:
        print(f"source_delta: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
