from pathlib import Path
import json,hashlib,collections
B=Path(__file__).parent.resolve();p=B/'coverage-novelty-adjudication-10-read-ledger.json';j=json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();groups=collections.defaultdict(list)
for x in j['text_slices']:groups[x['path']].append(x)
checks=[]
for x in j['text_inputs']:
 pth=Path(x['file']);s=pth.read_text();rows=groups[str(pth)];pairs=[(r['start'],r['end']) for r in rows];complete=pairs[0][0]==0 and pairs[-1][1]==len(s) and all(a[1]==b[0] for a,b in zip(pairs,pairs[1:]));valid=all(0<r['end']-r['start']<=6000 and r['output_cap_tokens']>=4000 and r['byte_sha256']==H(pth) and r['slice_sha256']==hashlib.sha256(s[r['start']:r['end']].encode()).hexdigest() for r in rows)
 checks.append({'file':str(pth),'sha256':H(pth),'slice_count':len(rows),'complete':complete,'all_slice_hashes_bounds_caps_match':valid,'pass':complete and valid and H(pth)==x['byte_sha256'] and len(s)==x['unicode_char_length']})
images=[{'file':x['file'],'pass':x['fully_inspected'] and H(Path(x['file']))==x['byte_sha256']} for x in j['image_inputs']];out={'ledger_sha256':H(p),'text_inputs':checks,'images':images,'text_slices':sum(len(v) for v in groups.values()),'all_passed':all(x['pass'] for x in checks+images) and not j['forbidden_inputs_read'],'note':'Verifies declared exact complete delivery, per-slice hashes and caps. Raw actual tool transcripts are retained separately; no filesystem-isolation claim.'};(B/'novelty10-delivery-validation.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'all_passed':out['all_passed'],'text_files':len(checks),'slices':out['text_slices'],'images':len(images)}))
