import importlib.util
from pathlib import Path
import tempfile
import unittest

PATH = Path(__file__).resolve().parents[1]/'taskdock/product-root/evals/continuity/fixture.py'
spec = importlib.util.spec_from_file_location('continuity_fixture', PATH)
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)


class ContinuityFixtureTests(unittest.TestCase):
    def test_raw_start_has_no_prebuilt_task_records(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)/'task'
            fixture.prepare(root)
            self.assertEqual([p.name for p in root.iterdir()], ['raw'])
            before = fixture.snapshot(root)
            with self.assertRaises(ValueError):
                fixture.prepare(root)
            self.assertEqual(fixture.snapshot(root), before)

    def test_advance_preserves_originals_and_adds_new_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, moved = Path(tmp)/'task', Path(tmp)/'moved'
            fixture.prepare(root)
            before = fixture.snapshot(root)
            fixture.advance(root, moved)
            after = fixture.snapshot(moved)
            self.assertFalse(root.exists())
            for path, data in before.items():
                self.assertEqual(after[path], data)
            self.assertIn('raw/unapproved-v3.md', after)
            self.assertIn('raw/decision-2026-09-19.txt', after)

    def test_snapshot_detects_same_filename_changed_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)/'task'
            fixture.prepare(root)
            before = fixture.snapshot(root)
            (root/'raw/approved-v2.md').write_text('not the approved bytes', encoding='utf-8')
            self.assertNotEqual(before, fixture.snapshot(root))


if __name__ == '__main__':
    unittest.main()
