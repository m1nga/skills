#!/usr/bin/env python3
"""Exercise a valid contract and a boolean budget without starting an agent loop."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parents[1] / 'loop-system-architect'
contract = json.loads((root / 'assets/loop.contract.minimal-example.json').read_text())
with tempfile.TemporaryDirectory(prefix='loop-budget-demo-', dir=Path.cwd()) as folder:
    path = Path(folder) / 'contract.json'
    for label, value, should_pass in [('valid integer budget', 12, True),
                                       ('boolean budget', True, False)]:
        contract['budgets']['max_turns'] = value
        path.write_text(json.dumps(contract), encoding='utf-8')
        result = subprocess.run([sys.executable, str(root / 'scripts/loop_lint.py'),
                                 str(path), '--json'], capture_output=True, text=True)
        verdict = json.loads(result.stdout)
        if should_pass:
            assert result.returncode == 0, verdict
        else:
            assert result.returncode != 0 and 'max_turns' in result.stdout, verdict
        print('PASS:', label, 'accepted.' if should_pass else 'rejected.')
print('This checks contract inputs. It does not start a scheduler or prove runtime recovery.')
