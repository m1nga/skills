import importlib.util
import pathlib
import threading
import time
import unittest
from unittest.mock import patch
spec=importlib.util.spec_from_file_location('redbot_video',pathlib.Path(__file__).resolve().parents[1]/'connector/video.py')
v=importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
class VideoTests(unittest.TestCase):
    def test_urls(self):
        for u in ['http://sns-video.xhscdn.com/a','https://localhost/a','https://xhscdn.com.evil.com/a','https://u:p@sns-video.xhscdn.com/a','https://sns-video.xhscdn.com:444/a']:
            with self.assertRaises(v.VideoError): v.resolve(u)
        with patch.object(v.socket,'getaddrinfo',return_value=[(None,None,None,None,('127.0.0.1',443))]):
            with self.assertRaises(v.VideoError): v.resolve('https://sns-video.xhscdn.com/a')
    def test_cancel_timeout(self):
        e=threading.Event(); e.set()
        with self.assertRaises(v.VideoError): v.check(e,time.monotonic()+10)
        with self.assertRaises(v.VideoError): v.check(threading.Event(),time.monotonic()-1)
    def test_source_version_excludes_rotating_signature(self):
        note={'video':{'media':{'videoId':123,'video':{'md5':'abc','duration':10},'stream':{'h264':[{'masterUrl':'https://sns-video.xhscdn.com/a?sign=one','duration':10000}]}}}}
        first=v.select_source(note)[2]
        note['video']['media']['stream']['h264'][0]['masterUrl']='https://sns-video.xhscdn.com/a?sign=two'
        self.assertEqual(first,v.select_source(note)[2])
        note['video']['media']['video']['md5']='changed'
        self.assertNotEqual(first,v.select_source(note)[2])
    def test_protected_and_long(self):
        with self.assertRaises(v.VideoError): v.select_source({'video':{'media':{'video':{'drmType':1}}}})
        with self.assertRaises(v.VideoError): v.select_source({'video':{'media':{'stream':{'h264':[{'masterUrl':'x','duration':601000}]}}}})
    def test_current_platform_stream_labels_use_mp4_container(self):
        note={'video':{'media':{'video':{'duration':23},'stream':{
            'EF4':[{'masterUrl':'https://sns-video.xhscdn.com/large','format':'mp4','duration':22453,'size':2126960}],
            'EF5':[{'masterUrl':'https://sns-video.xhscdn.com/small','format':'mp4','duration':22453,'size':1780392}],
            'EF6':[], 'unknown':[{'masterUrl':'https://sns-video.xhscdn.com/playlist','format':'m3u8','size':1}],
        }}}}
        url,duration,_=v.select_source(note)
        self.assertEqual(url,'https://sns-video.xhscdn.com/small')
        self.assertEqual(duration,22.453)
        note['video']['media']['video']['drmType']=1
        with self.assertRaises(v.VideoError) as error:v.select_source(note)
        self.assertEqual(error.exception.code,'video_protected')
if __name__=='__main__': unittest.main()

class VideoSessionTests(unittest.TestCase):
    def test_session_reads_only_own_selected_save(self):
        import tempfile
        from unittest.mock import Mock
        spec=importlib.util.spec_from_file_location('video_service',pathlib.Path(__file__).resolve().parents[1]/'connector/service.py')
        service=importlib.util.module_from_spec(spec);spec.loader.exec_module(service)
        with tempfile.TemporaryDirectory() as folder:
            directory=pathlib.Path(folder); backend=Mock()
            session=service.Session(directory,{'id':'session'},backend)
            session.state='connected'
            nid='a'*24
            with self.assertRaises(service.Problem):session.read_video(nid)
            backend.request.assert_not_called()
            session.library['items']=[{'id':nid,'type':'video'}]
            service.atomic(directory/'source-tokens.json',{nid:'private-token'})
            note={'noteId':nid,'desc':'saved caption','video':{}}
            backend.request.return_value={'note':note}
            result={'complete':True,'transcript':[{'start':0,'end':1,'text':'speech'}],'frames':[],'coverage':{'audio':'transcribed','frames':'sampled_ocr','visual':'not_performed'}}
            with patch.object(session,'verify'),patch.object(service.video,'analyze',return_value=result) as analyze:
                session.read_video(nid)
                self.assertEqual(analyze.call_args[0][0],note)
            data=(directory/'library.json').read_text()
            self.assertNotIn('private-token',data)
            self.assertEqual(session.library['items'][0]['videoAnalysis']['transcript'][0]['text'],'speech')

    def test_video_empty_caption_and_invalid_identity(self):
        import tempfile
        from unittest.mock import Mock
        spec=importlib.util.spec_from_file_location('empty_video_service',pathlib.Path(__file__).resolve().parents[1]/'connector/service.py')
        service=importlib.util.module_from_spec(spec);spec.loader.exec_module(service)
        with tempfile.TemporaryDirectory() as folder:
            directory=pathlib.Path(folder);backend=Mock();nid='c'*24
            session=service.Session(directory,{'id':'s'},backend);session.state='connected'
            item={'id':nid,'type':'video'};session.library['items']=[item]
            service.atomic(directory/'source-tokens.json',{nid:'private-token'})
            backend.request.return_value={'feed_id':nid,'data':{'note':{'noteId':nid,'desc':'','video':{}}}}
            result={'complete':True,'transcript':[{'text':'Actual speech'}],'frames':[]}
            with patch.object(session,'verify'),patch.object(service.video,'analyze',return_value=result):session.read_video(nid)
            self.assertEqual(item['contentReadStatus'],'ready');self.assertTrue(item['hasContent'])
            self.assertEqual(item['videoAnalysis']['transcript'],[{'text':'Actual speech'}])
            backend.request.return_value={'data':{'note':{'noteId':'','desc':''}}}
            with patch.object(session,'verify'),patch.object(service.video,'analyze') as analyze:
                with self.assertRaises(service.Problem) as error:session.read_video(nid)
                analyze.assert_not_called()
            self.assertEqual(error.exception.code,'source_content_invalid')
            self.assertEqual(item['videoAnalysis']['transcript'],[{'text':'Actual speech'}])
            self.assertEqual(item['contentReadStatus'],'failed')

class StaticAndCapacityTests(unittest.TestCase):
    def service(self):
        spec=importlib.util.spec_from_file_location('video_static_service',pathlib.Path(__file__).resolve().parents[1]/'connector/service.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
    def test_static_vendor_and_traversal(self):
        import tempfile
        s=self.service()
        with tempfile.TemporaryDirectory() as folder,tempfile.TemporaryDirectory() as outside:
            app=pathlib.Path(folder); (app/'vendor').mkdir();(app/'vendor/tool.mjs').write_text('export {}');(app/'vendor/tool.wasm').write_bytes(b'wasm');(app/'manifest.webmanifest').write_text('{}')
            secret=pathlib.Path(outside)/'private.json';secret.write_text('private');(app/'vendor/leak.json').symlink_to(secret)
            with patch.object(s,'APP',app):
                self.assertEqual(s.static_asset('/manifest.webmanifest')[1],'application/manifest+json');self.assertIn('javascript',s.static_asset('/vendor/tool.mjs')[1]); self.assertEqual(s.static_asset('/vendor/tool.wasm')[1],'application/wasm')
                for path in ['/vendor/../../private.json','/vendor/%2e%2e/%2e%2e/private.json','/vendor/leak.json','/.hidden.json','/connector/service.py']:
                    with self.assertRaises(s.Problem):s.static_asset(path)
    def test_video_global_slot_releases_after_failure(self):
        import tempfile
        from unittest.mock import Mock
        s=self.service(); started=threading.Event();stop=threading.Event()
        with tempfile.TemporaryDirectory() as folder:
            a=s.Session(pathlib.Path(folder)/'a',{'id':'a'},Mock());b=s.Session(pathlib.Path(folder)/'b',{'id':'b'},Mock())
            def work():started.set();stop.wait(2)
            a.start('video',work);self.assertTrue(started.wait(1))
            with self.assertRaises(s.Problem) as error:b.start('video',lambda:None)
            self.assertEqual(error.exception.code,'video_busy');stop.set();a.worker.join(2)
            b.start('video',lambda:None);b.worker.join(2);self.assertEqual(b.job['state'],'done')

class RefreshAndSourceTests(unittest.TestCase):
    def test_http_upgrade_only_known_cdns(self):
        self.assertEqual(v.normalize_source_url('http://sns-video.xhscdn.com/a?sign=private'),'https://sns-video.xhscdn.com/a?sign=private')
        for url in ['http://localhost/a','http://sns-video.xhscdn.com.evil.com/a','http://u:p@sns-video.xhscdn.com/a','http://sns-video.xhscdn.com:8080/a']:
            with self.assertRaises(v.VideoError):v.normalize_source_url(url)
    def test_refresh_failures_retain_last_success_and_success_clears_error(self):
        import tempfile
        from unittest.mock import Mock
        spec=importlib.util.spec_from_file_location('refresh_service',pathlib.Path(__file__).resolve().parents[1]/'connector/service.py')
        service=importlib.util.module_from_spec(spec);spec.loader.exec_module(service)
        with tempfile.TemporaryDirectory() as folder:
            directory=pathlib.Path(folder);backend=Mock();nid='b'*24
            session=service.Session(directory,{'id':'s'},backend);session.state='connected'
            prior={'complete':True,'readAt':'original-time','sourceVersion':'original-version','transcript':[{'start':0,'end':1,'text':'valuable prior transcript'}],'frames':[]}
            item={'id':nid,'type':'video','videoAnalysis':prior.copy(),'coverage':'video_audio_and_sampled_ocr'};session.library['items']=[item]
            service.atomic(directory/'source-tokens.json',{nid:'private-token'})
            backend.request.return_value={'feed_id':nid,'data':{'note':{'noteId':nid,'desc':'new caption'},'comments':{}}}
            for stage in ('verify','detail','analyze','partial'):
                with patch.object(session,'verify') as verify,patch.object(service.video,'analyze',return_value={'complete':False}) as analyze:
                    if stage=='verify':verify.side_effect=service.Problem('sign_in_required',401)
                    if stage=='detail':backend.request.side_effect=service.Problem('source_unavailable',502)
                    else:backend.request.side_effect=None
                    if stage=='analyze':analyze.side_effect=service.video.VideoError('video_timeout')
                    with self.assertRaises(service.Problem):session.read_video(nid)
                kept=item['videoAnalysis'];self.assertEqual(kept['transcript'],prior['transcript']);self.assertEqual(kept['readAt'],'original-time');self.assertEqual(kept['sourceVersion'],'original-version');self.assertTrue(kept['lastRefreshError']['retainedPrevious'])
            with patch.object(session,'verify'),patch.object(service.video,'analyze',return_value={**prior,'lastRefreshError':{'code':'old'},'cached':True}):session.read_video(nid)
            self.assertNotIn('lastRefreshError',item['videoAnalysis'])
