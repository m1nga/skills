import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "source_delta.py"


def row(key, revision="1", ref=None):
    return {"id": key, "revision": revision, "ref": ref or f"notes/{key}.html"}


class SourceDeltaTest(unittest.TestCase):
    def run_delta(self, previous, current, *args, scope="saved", current_scope=None):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            before = root / "previous.json"
            after = root / "current.json"
            before.write_text(json.dumps({
                "scope": scope, "coverage": "complete", "records": previous,
            }), encoding="utf-8")
            after.write_text(json.dumps({
                "scope": current_scope or scope, "coverage": "partial", "records": current,
            }), encoding="utf-8")
            originals = (before.read_bytes(), after.read_bytes())
            result = subprocess.run(
                [sys.executable, str(SCRIPT), before.name, after.name, *args],
                cwd=root, capture_output=True, text=True, check=False,
            )
            self.assertEqual(originals, (before.read_bytes(), after.read_bytes()))
            self.assertEqual({p.name for p in root.iterdir()}, {before.name, after.name})
            return result

    def test_change_reference_absence_and_paging(self):
        previous = [row("unchanged"), row("new-version"), row("moved"), row("absent")]
        current = [
            row("unchanged"), row("new-version", "2"), row("moved", ref="elsewhere.html"),
            row("added"),
        ]
        first = self.run_delta(previous, current, "--limit", "2")
        self.assertEqual(first.returncode, 0, first.stderr)
        delta = json.loads(first.stdout)
        self.assertEqual(delta["counts"]["changed"], 2)
        self.assertEqual(delta["counts"]["unchanged"], 1)
        self.assertEqual(delta["current_coverage"], "partial")
        self.assertEqual(delta["next_offset"], 2)
        second = self.run_delta(previous, current, "--limit", "2", "--offset", "2")
        last = json.loads(second.stdout)
        self.assertIsNone(last["next_offset"])
        combined = delta["records"] + last["records"]
        self.assertEqual([(r["id"], r["status"]) for r in combined], [
            ("added", "added"), ("moved", "changed"), ("new-version", "changed"),
            ("absent", "not_seen"),
        ])
        self.assertEqual(combined[1]["ref"], "elsewhere.html")

    def test_conflicting_duplicate_stops(self):
        result = self.run_delta([], [row("a"), row("a", "2")])
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("conflicting duplicate", result.stderr)

    def test_identical_duplicate_collapses(self):
        result = self.run_delta([], [row("a"), row("a")])
        delta = json.loads(result.stdout)
        self.assertEqual(delta["counts"]["added"], 1)
        self.assertEqual(delta["counts"]["current_duplicate_copies"], 1)

    def test_mismatched_scopes_stop(self):
        result = self.run_delta([row("a")], [row("a")], current_scope="other-library")
        self.assertEqual(result.returncode, 2)
        self.assertIn("scopes differ", result.stderr)

    def test_additional_payload_is_rejected(self):
        result = self.run_delta([], [dict(row("a"), body="A full source body")])
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("exactly id, revision and ref", result.stderr)

    def test_out_of_range_page_is_explicit(self):
        result = self.run_delta([], [row("a")], "--offset", "2")
        self.assertEqual(result.returncode, 2)
        self.assertIn("beyond 1 differences", result.stderr)


if __name__ == "__main__":
    unittest.main()
