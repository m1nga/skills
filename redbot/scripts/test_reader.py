import importlib.util,json,tempfile,unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('reader',Path(__file__).with_name('read_library.py'));reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
class ReaderTest(unittest.TestCase):
 def setUp(self):
  self.d={'items':[{'id':'a','title':'Clear first task','url':'https://example.org/a','research':{'points':[['Recovery','Keep invalid input editable.']]}},{'id':'b','title':'First task video','url':'https://example.org/b'},{'id':'c','title':'First task removed'}],'annotations':{'c':{'trashed':True}},'guides':[]}
 def test_read_is_unchanged_and_shortlist_then_exact_source(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'backup.json';p.write_text(json.dumps(self.d));before=p.read_bytes();x=reader.read(p)
   self.assertEqual(reader.select(x,'recovery')['matches'][0]['id'],'a');self.assertEqual(reader.select(x,item_id='a')['item']['research']['points'][0][0],'Recovery');self.assertEqual(p.read_bytes(),before)
 def test_title_only_and_removed_source_boundaries(self):
  rows=reader.select(self.d,'first task')['matches'];self.assertEqual({r['id'] for r in rows},{'a','b'});self.assertEqual(next(r for r in rows if r['id']=='b')['status'],'needs_reading')
  with self.assertRaises(ValueError):reader.select(self.d,item_id='c')
 def test_bad_input_is_not_a_silent_empty_library(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'bad.json';p.write_text('{}')
   with self.assertRaises(ValueError):reader.read(p)
 def test_goal_constraints_reject_dessert_and_use_synonym_evidence(self):
  d={'items':[{'id':'dessert','title':'最好吃的焦糖布蕾','description':'普通甜点制作步骤。'},{'id':'lunch','title':'减脂午餐','description':'减脂午餐食谱：食材与制作步骤。'}]}
  rows=reader.select(d,'我想自己做饭，有什么适合减肥吃的')['matches'];self.assertEqual([r['id'] for r in rows],['lunch']);self.assertEqual(rows[0]['goal_assessment']['status'],'supported');self.assertEqual(rows[0]['goal_assessment']['evidence'][0]['basis'],'source_claim')
  d['items'][1]['description']='这不是减脂餐，只是普通甜点食谱。';self.assertEqual(reader.select(d,'减肥食谱')['matches'],[])
 def test_unknown_titles_and_required_unsupported_constraints_are_conservative(self):
  self.assertEqual(reader.goal_assessment('减肥做饭',{'title':'减脂午餐'})['status'],'insufficient')
  self.assertEqual(reader.goal_assessment('减肥做饭',{'title':'减脂食谱'})['status'],'unknown')
  self.assertEqual(reader.goal_assessment('减脂食谱，必须适合肾病患者',{'description':'减脂食谱制作步骤。'})['status'],'insufficient')
  self.assertEqual(reader.goal_assessment('不要钱的工具',{'description':'免费试用后收费。'})['status'],'conflict')
  self.assertEqual(reader.goal_assessment('我不减肥',{'description':'减脂午餐食谱。'})['status'],'conflict')
 def test_video_text_search_exact_item_keeps_timestamps_and_drops_private_fields(self):
  x={'id':'v','title':'视频','videoAnalysis':{'transcript':[{'start':1,'end':4,'text':'咖啡研磨与冲煮。','url':'https://secret'}],'frames':[{'at':3,'text':[{'text':'水温参数','confidence':'.9'}],'path':'/private/frame.png'}],'coverage':{'audio':'transcribed','frames':'sampled_ocr','visual':'not_performed'},'complete':False,'error':'video_tool_failed','signedURL':'https://secret','lastRefreshError':{'code':'video_timeout','at':'2026-11-04T01:00:00Z','raw':'secret'}}}
  d={'items':[x]};self.assertEqual(reader.select(d,'咖啡')['matches'][0]['id'],'v');v=reader.select(d,item_id='v')['item']['videoAnalysis'];self.assertEqual(v['transcript'][0]['start'],1);self.assertEqual(v['frames'][0]['text'][0]['text'],'水温参数');self.assertFalse(v['complete']);self.assertEqual(v['lastRefreshError']['code'],'video_timeout');self.assertTrue(v['lastRefreshError']['retainedPrevious']);self.assertNotIn('secret',json.dumps(v));self.assertNotIn('/private',json.dumps(v))
 def test_large_video_item_retains_structure_with_explicit_truncation(self):
  d={'items':[{'id':'large','title':'video','videoAnalysis':{'transcript':[{'start':i,'end':i+1,'text':'x'*4000} for i in range(30)]}}]};out=reader.select(d,item_id='large');self.assertTrue(out['truncated']);self.assertIsInstance(out['item']['videoAnalysis'],dict);self.assertIsInstance(out['item']['videoAnalysis']['transcript'],list)
if __name__=='__main__':unittest.main()
