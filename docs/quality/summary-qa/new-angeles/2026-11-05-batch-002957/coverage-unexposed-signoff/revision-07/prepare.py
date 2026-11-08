from pathlib import Path
import json,hashlib,sys
out=Path(__file__).parent;own=out.parent;base=own.parent;ov,nv,prevname=sys.argv[1:4];prev=own/prevname
(out/'read-chunk.py').write_bytes((prev/'read-chunk.py').read_bytes());(out/'text-receipts.jsonl').write_text('')
def walk(a,b,path=''):
 if a==b:return []
 if isinstance(a,dict) and isinstance(b,dict):
  r=[]
  for k in b:r+=walk(a[k],b[k],path+'/'+str(k)) if k in a else [{'path':path+'/'+str(k),'change':'added','new':b[k]}]
  return r+[{'path':path+'/'+str(k),'change':'removed'} for k in a if k not in b]
 if isinstance(a,list) and isinstance(b,list):
  if all(isinstance(x,dict) and 'id' in x for x in a+b):return walk({x['id']:x for x in a},{x['id']:x for x in b},path)
  r=[]
  for i in range(min(len(a),len(b))):r+=walk(a[i],b[i],path+'/'+str(i))
  return r+[{'path':path+'/'+str(i),'change':'added','new':b[i]} for i in range(len(a),len(b))]+[{'path':path+'/'+str(i),'change':'removed'} for i in range(len(b),len(a))]
 return [{'path':path,'change':'changed','new':b}]
checks=[]
for manifest in [own/'all-input-hashes.json',own/'output-hashes.json',prev/'input-hashes.json',prev/'output-hashes.json']:
 for x in json.loads(manifest.read_text()):
  p=Path(x['path']);assert hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256'];checks.append({'path':str(p),'sha256':x['sha256'],'unchanged':True})
(out/'reuse-hash-verification.json').write_text(json.dumps(checks,indent=2)+'\n');inputs=[];summ=[]
for name in ['questions.json','answer-key.json','asked-clause-map.json','coverage-map.json','coverage-ledger.json','version-changes.json','input-manifest.json']:
 p=base/('expanded-candidate-'+nv)/name;a=json.loads((base/('expanded-candidate-'+ov)/name).read_text());b=json.loads(p.read_text());d=walk(a,b);dp=out/(name[:-5]+'-delta.json');dp.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');inputs.append({'path':str(p),'chars':len(p.read_text()),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()});summ.append({'name':name,'changed_units':len(d),'delta_chars':len(dp.read_text())})
(out/'input-hashes.json').write_text(json.dumps(inputs,indent=2)+'\n');print(json.dumps({'version':nv,'previous_hash_checks':len(checks),'deltas':summ},indent=2))
