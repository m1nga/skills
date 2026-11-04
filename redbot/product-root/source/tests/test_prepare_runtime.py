import hashlib
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
import urllib.error


SPEC = importlib.util.spec_from_file_location(
    "prepare_runtime", Path(__file__).resolve().parents[1] / "scripts" / "prepare-runtime.py"
)
runtime = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runtime)


class PrepareRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.target = Path(self.directory.name) / runtime.ASSET
        self.payload = b"synthetic WASM fixture"
        self.expected = {
            "bytes": len(self.payload),
            "sha256": hashlib.sha256(self.payload).hexdigest(),
        }

    def assert_preserved(self):
        self.assertEqual(self.target.read_bytes(), self.payload)
        self.assertEqual(list(self.target.parent.iterdir()), [self.target])

    def test_verified_existing_file_never_opens_network(self):
        self.target.write_bytes(self.payload)
        opener = Mock(side_effect=AssertionError("network must not be used"))
        self.assertIn("skipped", runtime.prepare(self.target, self.expected, opener=opener))
        opener.assert_not_called()

    def test_missing_file_download_is_verified_and_atomically_installed(self):
        opener = Mock(return_value=io.BytesIO(self.payload))
        runtime.prepare(self.target, self.expected, opener=opener)
        opener.assert_called_once_with(runtime.SOURCE, timeout=runtime.SOCKET_TIMEOUT)
        self.assert_preserved()

    def test_invalid_existing_requires_explicit_repair(self):
        self.target.write_bytes(b"broken")
        opener = Mock()
        with self.assertRaisesRegex(ValueError, "--repair"):
            runtime.prepare(self.target, self.expected, opener=opener)
        opener.assert_not_called()
        self.assertEqual(self.target.read_bytes(), b"broken")

    def test_network_failure_during_repair_preserves_verified_file(self):
        self.target.write_bytes(self.payload)
        opener = Mock(side_effect=urllib.error.URLError("synthetic connection failure"))
        with self.assertRaises(urllib.error.URLError):
            runtime.prepare(self.target, self.expected, repair=True, opener=opener)
        self.assert_preserved()

    def test_interrupted_transfer_removes_partial_file_and_preserves_original(self):
        self.target.write_bytes(self.payload)
        response = Mock()
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)
        response.read1.side_effect = [self.payload[:4], TimeoutError("synthetic read timeout")]
        with self.assertRaises(TimeoutError):
            runtime.prepare(self.target, self.expected, repair=True,
                            opener=Mock(return_value=response))
        self.assert_preserved()

    def test_failed_missing_download_leaves_no_artifact(self):
        with self.assertRaises(ValueError):
            runtime.prepare(self.target, self.expected, opener=Mock(return_value=io.BytesIO(b"short")))
        self.assertEqual(list(self.target.parent.iterdir()), [])

    def test_bad_hash_short_and_oversize_repair_preserve_verified_file(self):
        self.target.write_bytes(self.payload)
        for payload in (b"x" * len(self.payload), self.payload[:-1], self.payload + b"x"):
            with self.subTest(payload=payload):
                with self.assertRaises(ValueError):
                    runtime.prepare(self.target, self.expected, repair=True,
                                    opener=Mock(return_value=io.BytesIO(payload)))
                self.assert_preserved()

    def test_total_deadline_failure_preserves_verified_file(self):
        self.target.write_bytes(self.payload)
        with patch.object(runtime.time, "monotonic", side_effect=[0, runtime.DOWNLOAD_SECONDS + 1]):
            with self.assertRaises(TimeoutError):
                runtime.prepare(self.target, self.expected, repair=True,
                                opener=Mock(return_value=io.BytesIO(self.payload)))
        self.assert_preserved()

    def test_explicit_repair_replaces_corrupt_file_after_verification(self):
        self.target.write_bytes(b"broken")
        runtime.prepare(self.target, self.expected, repair=True,
                        opener=Mock(return_value=io.BytesIO(self.payload)))
        self.assert_preserved()


if __name__ == "__main__":
    unittest.main()
