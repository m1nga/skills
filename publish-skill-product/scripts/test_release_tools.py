"""Offline regression checks using temporary repositories and API fixtures."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest


def module(name):
    spec=importlib.util.spec_from_file_location(name, Path(__file__).with_name(name+'.py'))
    obj=importlib.util.module_from_spec(spec); spec.loader.exec_module(obj); return obj

release=module('check_release_source'); discovery=module('discovery_snapshot')

class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)
        self.git('init','-q');self.git('config','user.name','Fixture');self.git('config','user.email','fixture@example.invalid')
        for name in ('sample','other'):
            (self.root/name/'agents').mkdir(parents=True)
            for path in ('SKILL.md','README.md','agents/openai.yaml'):
                (self.root/name/path).write_text('fixture\n')
        (self.root/'products.json').write_text(json.dumps({'products':[{'name':'sample'},{'name':'other'}]}))
        (self.root/'LICENSE').write_text('fixture license\n');self.git('add','.');self.git('commit','-qm','fixture')
    def tearDown(self): self.tmp.cleanup()
    def git(self,*args): return subprocess.check_output(['git','-C',str(self.root),*args],text=True)
    def test_clean_source(self): self.assertEqual(release.check(self.root,'sample'),[])
    def test_unrelated_dirty_allowed(self):
        (self.root/'other/SKILL.md').write_text('user draft');self.assertEqual(release.check(self.root,'sample'),[])
    def test_dirty_target_blocked(self):
        (self.root/'sample/SKILL.md').write_text('user draft');self.assertTrue(release.check(self.root,'sample'))
    def test_staged_target_blocked(self):
        (self.root/'sample/SKILL.md').write_text('user draft');self.git('add','sample');self.assertTrue(release.check(self.root,'sample'))
    def test_untracked_target_blocked(self):
        (self.root/'sample/new.py').write_text('private draft');self.assertTrue(release.check(self.root,'sample'))
    def test_dirty_manifest_blocked(self):
        (self.root/'products.json').write_text('{}');self.assertTrue(release.check(self.root,'sample'))
    def test_path_traversal_blocked(self): self.assertTrue(release.check(self.root,'../sample'))
    def test_unregistered_blocked(self): self.assertTrue(release.check(self.root,'new'))

class DiscoveryTests(unittest.TestCase):
    def test_failed_api_is_unknown(self):
        def fail(*a,**k):return {'status':'unavailable','data':None}
        record=discovery.collect('a/b',['fixed query'],True,fail)
        self.assertEqual(record['search'][0]['status'],'unavailable');self.assertIsNone(record['search'][0]['rank'])
        self.assertNotIn('stargazers_count',record['metadata']);self.assertEqual(record['attribution'],'unknown')
    def test_rank_and_no_result(self):
        def fake(endpoint,**kw):
            data=({'items':[{'full_name':'c/d'},{'full_name':'A/B'}]} if kw.get('q')=='find' else {'items':[]}) if endpoint=='search/repositories' else {'stargazers_count':0}
            return {'status':'ok','data':data}
        r=discovery.collect('a/b',['find','missing'],fetch=fake)
        self.assertEqual(r['search'][0]['rank'],2);self.assertEqual(r['search'][1]['status'],'not_found_in_top_20')
        self.assertEqual(r['metadata']['stargazers_count'],0);self.assertIsNone(r['metadata']['forks_count'])
    def test_incomplete_results_are_not_absence(self):
        def fake(*a,**k):return {'status':'ok','data':{'items':[],'incomplete_results':True}}
        self.assertEqual(discovery.collect('a/b',['q'],fetch=fake)['search'][0]['status'],'incomplete')
    def test_comparison_only_matches_fixed_queries(self):
        old={'repository':'a/b','search':[{'query':'q','status':'found','rank':2}]}
        new={'repository':'a/b','search':[{'query':'q','status':'found','rank':1},{'query':'new','status':'found','rank':1}]}
        comparison=discovery.compare(old,new)
        self.assertEqual(len(comparison['search']),1);self.assertEqual(comparison['causal_effect'],'not_established')
    def test_cross_repository_comparison_rejected(self):
        with self.assertRaises(ValueError):discovery.compare({'repository':'a/b'},{'repository':'a/c'})
    def test_existing_snapshot_not_overwritten(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'snapshot.json';p.write_text('original')
            result=subprocess.run(['python3',str(Path(__file__).with_name('discovery_snapshot.py')),'a/b','--out',str(p)],capture_output=True)
            self.assertNotEqual(result.returncode,0);self.assertEqual(p.read_text(),'original')

if __name__=='__main__':unittest.main()
