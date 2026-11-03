import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import os
import subprocess
import sys
import unittest
spec = importlib.util.spec_from_file_location('gap', Path(__file__).resolve().parents[1] / 'scripts/gap.py')
gap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gap)

class GapTests(unittest.TestCase):
    def setUp(self):
        base = Path(os.environ.get('BREAKINGGAP_TEST_ROOT', str(Path.cwd()))).resolve()
        base.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        (self.root / 'task.txt').write_text('evidence')
        self.c = dict(id='a', kind='advance', title='Paragraph', action='Write paragraph', done_when='Saved', pause_after='One paragraph', resume_hint='Read last line', project='p', source=dict(path='task.txt', sha256=hashlib.sha256(b'evidence').hexdigest()), state='ready', owner='human', authorized=True, interruptible=True, conflict_check='clear', minutes=dict(setup=1,work=3,wrap=1))
        self.data = dict(schema_version=1, project=dict(id='p',title='Project'), current_work=dict(title='Build',return_to='Review build',agent_status='running'), candidates=[self.c])
    def rec(self, minutes=7, intent='any'):
        return gap.recommend(self.root,self.data,minutes,intent)
    def test_budget(self):
        self.assertEqual(self.rec(6)['status'],'no_match')
        self.assertEqual(self.rec(7)['status'],'suggested')
    def test_filters(self):
        for key,value in [('state','held'),('owner','agent'),('conflict_check','conflict'),('authorized',False),('interruptible',False)]:
            old=self.c[key]; self.c[key]=value
            self.assertEqual(self.rec()['status'],'no_match',key)
            self.c[key]=old
        (self.root/'task.txt').write_text('changed')
        self.assertIn('stale_source',self.rec()['excluded'][0]['reasons'])
    def test_exact_intent(self):
        self.assertEqual(self.rec(intent='learn')['status'],'no_match')
        self.c['kind']='learn'
        self.assertEqual(self.rec(intent='learn')['chosen']['kind'],'learn')
    def test_empty_early_handback(self):
        self.data['candidates']=[]
        self.assertEqual(self.rec()['status'],'no_match')
        self.data['candidates']=[self.c]
        for status,expected in [('waiting_for_user','needs_attention'),('finished','ready_to_review')]:
            self.data['current_work']['agent_status']=status
            self.assertEqual(self.rec()['status'],expected)
            self.assertIsNone(self.rec()['chosen'])
    def test_idempotency_active_preservation(self):
        p=self.rec(); first=gap.start(self.root,p)
        self.assertEqual(first,gap.start(self.root,p))
        other=copy.deepcopy(p); other['chosen']['id']='b'
        with self.assertRaises(gap.GapError): gap.start(self.root,other)
        self.assertEqual(first['id'],gap.resume(self.root)['session']['id'])
    def test_notes_history(self):
        gap.start(self.root,self.rec())
        s=gap.checkpoint(self.root,'paused','准确 notes\nline 2','Read §2')
        self.assertEqual(s,gap.checkpoint(self.root,'paused','准确 notes\nline 2','Read §2'))
        self.assertEqual(gap.resume(self.root)['session']['notes'][0]['note'],'准确 notes\nline 2')
        gap.checkpoint(self.root,'done','Saved','Return')
        self.assertEqual(gap.resume(self.root)['session']['state'],'done')
        gap.start(self.root,self.rec())
        j=json.loads((self.root/'.breakinggap/session.json').read_text())
        self.assertEqual(j['history'][0]['state'],'done')
    def test_corrupt_preserved(self):
        (self.root/'.breakinggap').mkdir()
        p=self.root/'.breakinggap/session.json'; p.write_text('{broken')
        with self.assertRaises(gap.GapError): gap.start(self.root,self.rec())
        self.assertEqual(p.read_text(),'{broken')
    def test_unsafe_sources(self):
        for p in ('../task.txt',str(self.root/'task.txt')):
            self.c['source']['path']=p
            self.assertIn('unsafe_source',self.rec()['excluded'][0]['reasons'])
        try: (self.root/'link').symlink_to(self.root/'task.txt')
        except OSError: self.skipTest('Symlinks unavailable')
        self.c['source']['path']='link'
        self.assertIn('unsafe_source',self.rec()['excluded'][0]['reasons'])
    def test_changed_at_start(self):
        p=self.rec(); (self.root/'task.txt').write_text('new')
        with self.assertRaises(gap.GapError): gap.start(self.root,p)
        self.assertFalse((self.root/'.breakinggap/session.json').exists())
    def test_busy_preserved(self):
        (self.root/'.breakinggap').mkdir()
        p=self.root/'.breakinggap/session.lock'; p.write_text('unknown writer')
        with self.assertRaises(gap.GapError): gap.start(self.root,self.rec())
        self.assertEqual(p.read_text(),'unknown writer')
    def test_ranking(self):
        b=copy.deepcopy(self.c); b.update(id='b',project='other'); b['minutes']['work']=1
        self.data['candidates'].append(b)
        self.assertEqual(self.rec()['chosen']['id'],'a')
        b['project']='p'
        self.assertEqual(self.rec()['chosen']['id'],'b')

    def test_parseable_corruption_preserved(self):
        gap.start(self.root,self.rec())
        path=self.root/'.breakinggap/session.json'
        original=json.loads(path.read_text())
        variants=[]
        for field,value in [('notes',['bad']),('proposal',{}),('id',17)]:
            j=copy.deepcopy(original); j['session'][field]=value; variants.append(j)
        j=copy.deepcopy(original); del j['session']['proposal']['chosen']; variants.append(j)
        j=copy.deepcopy(original); j['history']=['bad']; variants.append(j)
        for j in variants:
            raw=json.dumps(j); path.write_text(raw)
            with self.assertRaises(gap.GapError): gap.resume(self.root)
            with self.assertRaises(gap.GapError): gap.checkpoint(self.root,'paused','note','next')
            self.assertEqual(path.read_text(),raw)
    def test_private_modes(self):
        gap.start(self.root,self.rec())
        if os.name!='nt':
            self.assertEqual((self.root/'.breakinggap').stat().st_mode & 0o777,0o700)
            self.assertEqual((self.root/'.breakinggap/session.json').stat().st_mode & 0o777,0o600)
    def test_runtime_cannot_be_source(self):
        (self.root/'.breakinggap').mkdir()
        (self.root/'.breakinggap/evidence').write_text('evidence')
        self.c['source']['path']='.breakinggap/evidence'
        self.assertIn('unsafe_source',self.rec()['excluded'][0]['reasons'])
    def test_cli_no_overwrite_and_json_error(self):
        inp=self.root/'input.json'; inp.write_text(json.dumps(self.data))
        script=Path(gap.__file__).resolve()
        def cli(out):
            return subprocess.run([sys.executable,str(script),'recommend','--root',str(self.root),'--input',str(inp),'--minutes','7','--out',str(out)],capture_output=True,text=True)
        for target in (inp,self.root/'task.txt',self.root/'.breakinggap/session.json',self.root/'.breakinggap/session.lock'):
            before=target.read_bytes() if target.exists() else None
            r=cli(target)
            self.assertNotEqual(r.returncode,0)
            self.assertEqual(json.loads(r.stdout)['status'],'error')
            self.assertEqual(target.read_bytes() if target.exists() else None,before)
        out=self.root/'proposal.json'
        self.assertEqual(cli(out).returncode,0)
        before=out.read_bytes()
        self.assertNotEqual(cli(out).returncode,0)
        self.assertEqual(out.read_bytes(),before)

if __name__=='__main__': unittest.main()
