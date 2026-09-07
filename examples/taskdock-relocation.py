#!/usr/bin/env python3
"""Run a disposable TaskDock move-and-resume demonstration in the current directory."""
import importlib.util
from pathlib import Path
import shutil
import tempfile

source = Path(__file__).resolve().parents[1] / 'taskdock/scripts/taskdock.py'
spec = importlib.util.spec_from_file_location('taskdock_demo_helper', source)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)

with tempfile.TemporaryDirectory(prefix='taskdock-demo-', dir=Path.cwd()) as folder:
    base = Path(folder)
    index = base / 'index/index.json'
    original = base / 'launch-review'
    created = helper.init_task('Launch review', 'Review a fictional launch brief', index,
                               path=original, language='en')
    (original / 'STATE.md').write_text('Next action: confirm the target customer.\n', encoding='utf-8')
    (original / 'brief.txt').write_text('Fictional product brief.\n', encoding='utf-8')
    before = (original / 'brief.txt').read_bytes()
    moved = base / 'renamed-launch-review'
    shutil.move(str(original), str(moved))
    found = helper.locate(index, identity=created['id'], roots=[base])
    assert found['status'] == 'found'
    assert Path(found['matches'][0]['path']) == moved
    assert helper.read_task(moved)['id'] == created['id']
    assert (moved / 'brief.txt').read_bytes() == before
    assert helper.check(moved)['status'] == 'pass'
    print('PASS: renamed folder found with the same task UUID.')
    print('PASS: existing brief preserved byte for byte.')
    print('Resume:', (moved / 'STATE.md').read_text().strip())
    shutil.copytree(moved, base / 'second-copy')
    duplicate = helper.locate(index, identity=created['id'], roots=[base])
    assert duplicate['status'] == 'ambiguous'
    print('PASS: two copies are reported as ambiguous; no copy silently selected.')
print('Demo complete. Its temporary task and private index were removed.')
