from pathlib import Path
import re,requests,concurrent.futures,datetime,json,hashlib
p=Path(__file__).parent
s=Path('rules/spirit-island.md').read_text(); js=(p/'catalog-cards.js').read_text()
items=[]
for l in js.splitlines():
 m=re.search(r'new (PowerCard|FearCard)\(ProductSet\.([^,]+), [^,]+, "([^"]+)"',l)
 if not m:continue
 typ,set_,name=m.groups()
 if name.lower() not in s.lower() and name!='Overseas Trade Seem Safer':continue
 if name=='Unrest':continue
 slug=re.sub('[^a-z_]','',name.lower().replace(' ','_'))
 filename=slug+'.jpg'
 if (p/filename).exists():continue
 u='https://sick.oberien.de/imgs/'+('fears/' if typ=='FearCard' else 'powers/')+filename
 items.append((filename,u,name,set_))
def fetch(kv):
 n,u,name,set_=kv
 try:
  r=requests.get(u,timeout=40);r.raise_for_status();(p/n).write_bytes(r.content)
  return {'file':n,'url':u,'capture_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sha256':hashlib.sha256(r.content).hexdigest(),'bytes':len(r.content),'card_title':name,'locator_set_only':set_}
 except Exception as e:return {'file':n,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
 for d in ex.map(fetch,items):
  with (p/'provenance.jsonl').open('a') as f:f.write(json.dumps(d)+'\n')
  print(d['file'], d.get('bytes',d.get('error')),flush=True)
