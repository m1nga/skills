"""Execute the publisher's actual packaging block with temporary source files."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which('rsync') and shutil.which('bash'), 'Publisher requires bash and rsync')
class OverlayTests(unittest.TestCase):
    def test_nested_readmes_are_shipped_but_root_contract_cannot_be_overridden(self):
        script = (ROOT/'scripts/publish-skill').read_text(encoding='utf-8')
        start = script.index('mkdir -p "$temp_root/product/skills/$skill"')
        end = script.index('jq -n', start)
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            files = {'source/sample/README.md': 'real root README', 'source/LICENSE': 'real license',
                     'source/sample/SKILL.md': 'skill',
                     'source/sample/product-root/README.md': 'must not replace root',
                     'source/sample/product-root/LICENSE': 'must not replace license',
                     'source/sample/product-root/SOURCE.json': 'must not forge source',
                     'source/sample/product-root/evals/README.md': 'evaluation instructions'}
            for name, content in files.items():
                path = base/name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding='utf-8')
            subprocess.run(['bash', '-euo', 'pipefail', '-c', 'temp_root="$1"; skill=sample\n' + script[start:end],
                            'publisher-test', str(base)], check=True)
            self.assertEqual((base/'product/README.md').read_text(), 'real root README')
            self.assertEqual((base/'product/LICENSE').read_text(), 'real license')
            self.assertFalse((base/'product/SOURCE.json').exists())
            self.assertEqual((base/'product/evals/README.md').read_text(), 'evaluation instructions')


if __name__ == '__main__':
    unittest.main()

class MetadataWriteTests(unittest.TestCase):
    def check_writes(self, drift):
        import json
        import os
        import sys
        script = (ROOT/'scripts/publish-skill').read_text(encoding='utf-8')
        block = script[script.index('current_meta='):script.index('\n"$repo_root/scripts/verify-published-skill"')]
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            gh = base/'gh'
            gh.write_text('#!' + sys.executable + '\n' + '''import json,os,sys
from pathlib import Path
args=sys.argv[1:]
with open(os.environ['CALL_LOG'],'a') as f: f.write(json.dumps(args)+'\\n')
if '--method' in args: print('{}')
elif args[1].endswith('/topics'): print('["a", "b"]')
else: print(json.dumps({'description': 'old' if os.environ['DRIFT']=='1' else 'same', 'has_issues':True, 'has_wiki':False}))
''', encoding='utf-8')
            gh.chmod(0o755)
            env = dict(os.environ, PATH=str(base)+os.pathsep+os.environ['PATH'], CALL_LOG=str(base/'calls'), DRIFT='1' if drift else '0')
            prefix = "target=owner/skill; description=same; product='{" + '"topics":["a","b"]' + "}'\n"
            subprocess.run(['bash','-euo','pipefail','-c',prefix+block], env=env, check=True, capture_output=True)
            return [json.loads(line) for line in (base/'calls').read_text().splitlines() if '--method' in line]

    def test_matching_metadata_uses_no_write_permissions(self):
        self.assertEqual(self.check_writes(False), [])

    def test_real_metadata_drift_is_not_silently_skipped(self):
        writes = self.check_writes(True)
        self.assertEqual(len(writes), 1)
        self.assertEqual(writes[0][1:3], ['--method','PATCH'])
