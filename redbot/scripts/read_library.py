#!/usr/bin/env python3
"""Read-only, bounded RedBot library reader; standard library only."""
import argparse,json,re,sys,urllib.request
from pathlib import Path

def read(path=None,live=False):
    if live:
        with urllib.request.urlopen('http://127.0.0.1:8766/api/library',timeout=5) as response:
            raw=response.read(45*1024*1024+1)
    else:
        p=Path(path).expanduser()
        if p.stat().st_size>45*1024*1024:raise ValueError('Backup exceeds 45 MB.')
        raw=p.read_bytes()
    if len(raw)>45*1024*1024:raise ValueError('Backup exceeds 45 MB.')
    d=json.loads(raw)
    if not isinstance(d,dict) or not isinstance(d.get('items'),list):raise ValueError('Expected a RedBot JSON backup with items.')
    return d

def video_evidence(item):
    """Only transcription/OCR and coverage; never copy source URLs or local frame paths."""
    v=item.get('videoAnalysis')
    if not isinstance(v,dict):return None
    def num(value):
        try:return max(0,float(value))
        except (TypeError,ValueError):return 0
    return {'transcript':[{'start':num(t.get('start')),'end':num(t.get('end')),'text':str(t.get('text',''))[:4000]} for t in v.get('transcript',[]) if isinstance(t,dict)][:20000],
      'frames':[{'at':num(f.get('at')),'text':[{'text':str(t.get('text',''))[:4000],'confidence':str(t.get('confidence',''))[:30]} for t in (f.get('text') or []) if isinstance(t,dict)][:200]} for f in v.get('frames',[]) if isinstance(f,dict)][:12],
      'coverage':{k:str((v.get('coverage') or {}).get(k,'unknown'))[:80] for k in ['audio','frames','visual']},
      'lastRefreshError':{'code':v['lastRefreshError']['code'],'at':str(v['lastRefreshError'].get('at',''))[:40],'retainedPrevious':True} if isinstance(v.get('lastRefreshError'),dict) and re.fullmatch('[a-z0-9_:-]{1,80}',str(v['lastRefreshError'].get('code','')),re.I) else None,
      'complete':v.get('complete') is True,'error':str(v.get('error','')) if re.fullmatch('[a-z0-9_:-]{0,80}',str(v.get('error','')),re.I) else 'unknown',
      'visualUnderstanding':False,'sourceVersion':v.get('sourceVersion','') if re.fullmatch('[a-fA-F0-9]{64}',str(v.get('sourceVersion',''))) else '',
      'sampling':{'allFrames':False,'maxFrames':12},'readAt':str(v.get('readAt',''))[:40]}

def source_text(x,note=''):
    research=x.get('research') or {};v=video_evidence(x) or {}
    return '\n'.join(str(s) for s in [x.get('summary',''),x.get('description',''),x.get('readingNotes',''),x.get('transcript',''),research.get('decision',''),*[' '.join(map(str,p)) for p in research.get('points',[]) if isinstance(p,list) and len(p)==2],*[t['text'] for t in v.get('transcript',[])],*[t['text'] for f in v.get('frames',[]) for t in f['text']],note] if s)

# These are explicitly bounded retrieval checks, not a general reasoning or nutrition engine.
CONCEPTS=[
 ('cooking',r'做饭|自己做|下厨|食谱|菜谱|烹饪|recipe|cooking',r'做饭|下厨|食谱|菜谱|做法|食材|制作步骤|recipe|cooking|ingredients',r'不适合做饭'),
 ('weight-loss',r'减肥|减脂|weight loss|fat loss',r'(?:减肥|减脂)(?:餐|食谱|午餐|晚餐|早餐|饮食|训练|计划)|(?:适合|帮助|用于)(?:减肥|减脂)|(?:weight|fat) loss (?:meal|recipe|diet|workout|plan)',r'(?:不|并非|不是)(?:适合|用于|帮助)?(?:减肥|减脂)|not (?:suitable for )?(?:weight|fat) loss'),
 ('free',r'免费|不要钱|\bfree\b',r'免费|不要钱|\bfree\b',r'(?:不|并非|不是)免费|not free|必须付费|需付费|试用.{0,12}(?:收费|付费)|免费.{0,12}(?:后收费|后需订阅)'),
 ('cheap',r'便宜|低成本|低预算|cheap|budget',r'便宜|低成本|低预算|平价|cheap|budget',r'昂贵|高成本|expensive'),
 ('no-equipment',r'无器械|不用器械|不需要器械|no equipment',r'无器械|不用器械|不需要器械|徒手|no equipment|bodyweight',r'需要哑铃|需用哑铃|必须.{0,12}器械|requires?.*(?:equipment|dumbbell)')]

def goal_assessment(query,x,note=''):
    required=[c for c in CONCEPTS if re.search(c[1],query,re.I) and not(c[0]=='cheap' and re.search('page|design|website|网页|设计|质感',query,re.I))]
    if re.search(r'(?:不|不要|无需)(?:减肥|减脂)',query):
        required=[c for c in required if c[0]!='weight-loss']
        required.append(('exclude:weight-loss','',r'(?:不|不要|无需)(?:减肥|减脂)',r'(?<!不)(?:减肥|减脂)'))
    for m in re.finditer(r'(?:不要|不含|不吃|排除|without|exclude)\s*([a-z][a-z -]{1,24}|[\u3400-\u9fff]{1,8})',query.replace('不要钱','免费').replace('不要减肥','').replace('不要减脂',''),re.I):
        term=re.split('[，。和或的]',m[1])[0].strip()
        if term and term not in ['钱','器械']:required.append(('exclude:'+term,'',r'(?:不含|不吃|不要|无|without|exclude)\s*'+re.escape(term),re.escape(term)))
    for m in re.finditer(r'(?:必须|仅限|不超过|只用|不使用)([^，。！？;；]{1,40})',query):
        rest=m[1]
        for c in CONCEPTS:rest=re.sub(c[1],'',rest,flags=re.I)
        if re.sub(r'且|并且|的|工具|食谱|训练|使用|是|要|来','',rest).strip():required.append(('unresolved:'+m[0],'',r'(?!)',r'(?!)'))
    body=source_text(x,note);title=str(x.get('title',''));evidence=[];missing=[];conflicts=[];title_support=True
    for key,_,positive,negative in required:
        found=next((s.strip() for s in re.split(r'(?<=[。！？.!?\n])',body) if re.search(positive,s,re.I)),None)
        # For exclusions, an explicit negative source statement wins over its noun mention.
        conflict=re.search(negative,body+' '+title,re.I) and not(key.startswith('exclude:') and found)
        if conflict:conflicts.append(key)
        elif found:evidence.append({'requirement':key,'text':found,'basis':'source_claim'})
        else:missing.append(key)
        title_support=title_support and bool(re.search(positive,title,re.I))
    status='conflict' if conflicts else 'insufficient' if missing and (body.strip() or not title_support) else 'unknown' if missing else 'supported'
    return {'status':status,'requirements':[c[0] for c in required],'evidence':evidence,'missing':missing,'conflicts':conflicts,'limit':'Source claims only; not independent verification or general natural-language reasoning.'}

def query_terms(query):
    q=re.sub(r'我想要?|自己|有什么|适合|吃的|帮我|怎么|如何|一些|一个|收藏|笔记',' ',query.lower())
    terms=re.findall(r'[a-z0-9_-]{2,}',q)
    chinese=re.findall(r'[\u3400-\u9fff]{2,}',q)
    vocabulary=['减肥','减脂','做饭','食谱','午餐','咖啡','设计','健身','训练','免费','便宜','无器械','视频','工具','工作流','记忆']
    terms.extend(t for t in vocabulary if t in q)
    terms.extend(chinese)
    if any(t in query for t in ['减肥','减脂']):terms.extend(['减肥','减脂'])
    return set(terms)

def select(d,query='',item_id=None,limit=8):
    ann=d.get('annotations') or {};rows=[x for x in d['items'] if isinstance(x,dict) and not ann.get(x.get('id'),{}).get('trashed') and not ann.get(x.get('id'),{}).get('archived')]
    if item_id:
        item=next((x for x in rows if x.get('id')==item_id),None)
        if not item:raise ValueError('Active save not found.')
        allowed=['id','title','url','author','description','summary','transcript','readingNotes','research','coverage','resources','anchors']
        out={k:item[k] for k in allowed if k in item}
        video=video_evidence(item)
        if video is not None:out['videoAnalysis']=video
        if query:out['goal_assessment']=goal_assessment(query,item,ann.get(item_id,{}).get('note',''))
        out['personal_note']=ann.get(item_id,{}).get('note','')
        out['related_guides']=[g for g in d.get('guides',[]) if item_id in g.get('sourceIds',[])]
        encoded=json.dumps(out,ensure_ascii=False)
        if len(encoded)>32000:
            def trim(value):
                if isinstance(value,str):return value[:1500]
                if isinstance(value,list):return [trim(v) for v in value[:8]]
                if isinstance(value,dict):return {k:trim(v) for k,v in value.items()}
                return value
            return {'item':trim(out),'truncated':True,'warning':'Read the named local backup for full detail; do not infer omitted material.'}
        return {'item':out,'truncated':False}
    terms=query_terms(query)
    result=[]
    for x in rows:
        note=ann.get(x.get('id'),{}).get('note','')
        body=str(x.get('title',''))+' '+source_text(x,note)
        score=sum(body.lower().count(t) for t in set(terms)) if terms else 1
        if not score:continue
        assessment=goal_assessment(query,x,note)
        if assessment['status'] in ['conflict','insufficient']:continue
        research=x.get('research') or {}
        readable=bool(source_text(x,note).strip())
        result.append({'id':x.get('id'),'title':x.get('title'),'url':x.get('url'),'status':'saved_text' if readable else 'needs_reading','score':score,'excerpt':body[:450],'goal_assessment':assessment})
    result.sort(key=lambda x:-x['score'])
    return {'mode':'lexical_shortlist','matches':result[:limit],'matched_count':len(result),'next':'Inspect a selected ID before recommending. No match is not proof of absence.'}

def main():
    p=argparse.ArgumentParser();p.add_argument('backup',nargs='?');p.add_argument('--live',action='store_true');p.add_argument('--query',default='');p.add_argument('--id');p.add_argument('--limit',type=int,default=8);a=p.parse_args()
    if bool(a.backup)==bool(a.live):p.error('Choose exactly one backup path or --live.')
    try:print(json.dumps(select(read(a.backup,a.live),a.query,a.id,max(1,min(a.limit,20))),ensure_ascii=False))
    except (OSError,ValueError,TypeError,AttributeError) as e:print(json.dumps({'error':str(e),'recovery':'Export a RedBot JSON backup or provide the correct active save ID.'}),file=sys.stderr);return 2
    return 0
if __name__=='__main__':raise SystemExit(main())
