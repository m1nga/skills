#!/usr/bin/env python3
"""Read-only runtime preflight. Presence/version is NOT authentication or a live eval."""
import json
import shutil
import subprocess

rows = []
for name in ('claude', 'codex'):
    executable = shutil.which(name)
    row = {'engine': name, 'executable_found': bool(executable), 'authenticated': None,
           'live_eval_executed': False}
    if executable:
        try:
            result = subprocess.run([executable, '--version'], capture_output=True, text=True, timeout=15)
            row['version'] = (result.stdout or result.stderr).strip()
            row['status'] = 'requires_authenticated_isolated_session' if result.returncode == 0 else 'version_check_failed'
        except (OSError, subprocess.TimeoutExpired) as error:
            row['status'] = 'version_check_failed'
            row['error'] = str(error)
    else:
        row['status'] = 'blocked_missing_runtime'
    rows.append(row)
print(json.dumps({'status': 'not_run', 'runtimes': rows,
                  'note': 'No model calls, credential reads, installations, or user configuration changes.'}, indent=2))
raise SystemExit(1)
