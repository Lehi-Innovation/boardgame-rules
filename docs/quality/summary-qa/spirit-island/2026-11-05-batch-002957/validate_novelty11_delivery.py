from pathlib import Path
import hashlib,json
B=Path(__file__).parent.resolve();h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=B/'coverage-novelty-adjudication-11-read-ledger.json';d=json.loads(p.read_text());checks=[]
for x in d['text_files']:
 f=Path(x['path']);s=f.read_text();rows=x['slices'];pairs=[r['range'] for r in rows]
 complete=bool(pairs) and pairs[0][0]==0 and pairs[-1][1]==len(s) and all(a[1]==b[0] for a,b in zip(pairs,pairs[1:]))
 valid=all(0<r['range'][1]-r['range'][0]<=6000 and r['output_cap_tokens']>=4000 and not r['truncated'] and hashlib.sha256(s[r['range'][0]:r['range'][1]].encode()).hexdigest()==r['slice_utf8_sha256'] for r in rows)
 checks.append({'file':str(f),'sha256':h(f),'slices':len(rows),'pass':complete and valid and h(f)==x['original_byte_sha256'] and len(s)==x['character_length']})
images=[{'file':x['path'],'pass':x['fully_viewed'] and h(Path(x['path']))==x['original_byte_sha256'] and x['viewed_region']==[0,0,*x['dimensions']]} for x in d['image_files']]
out={'ledger_sha256':h(p),'text_files':checks,'images':images,'all_passed':all(x['pass'] for x in checks+images) and not d['forbidden_inputs_read'],'text_slices':sum(x['slices'] for x in checks),'note':'Independent hash/range/cap completeness validation of declared delivery. Native image inspections and opaque runtime provenance retained separately; no isolation claim.'}
(B/'novelty11-delivery-validation.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'all_passed':out['all_passed'],'text_files':len(checks),'slices':out['text_slices'],'images':len(images)}))
assert out['all_passed']
