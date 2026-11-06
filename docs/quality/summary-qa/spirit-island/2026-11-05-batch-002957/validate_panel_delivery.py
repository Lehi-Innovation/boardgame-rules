from pathlib import Path
import json,hashlib,collections
B=Path(__file__).parent.resolve();h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();out=[]
for name in ['base-reachability-audit-01-read-ledger.json','original-panel-audit-01-read-ledger.json']:
 p=B/name;d=json.loads(p.read_text());groups=collections.defaultdict(list)
 for x in d['text_reads']:groups[(x['path'],x['original_byte_sha256'])].append(x)
 checks=[]
 for (original,sha),rows in groups.items():
  f=Path(rows[0].get('historical_original_preserved_at',original));s=f.read_text();pairs=[r['range'] for r in rows];complete=pairs[0][0]==0 and pairs[-1][1]==len(s) and all(a[1]==z[0] for a,z in zip(pairs,pairs[1:]))
  valid=all(0<r['range'][1]-r['range'][0]<=6000 and r['max_output_tokens']>=4000 and hashlib.sha256(s[r['range'][0]:r['range'][1]].encode()).hexdigest()==r['slice_utf8_sha256'] and len(s)==r['character_length'] for r in rows)
  checks.append({'path':original,'version_sha256':sha,'resolved_immutable_path':str(f),'slices':len(rows),'pass':h(f)==sha and complete and valid})
 images=[]
 for x in d.get('image_reads',[]):
  dims=x['native_dimensions'];regions=x['viewed_regions'];images.append({'path':x['path'],'pass':h(Path(x['path']))==x['original_byte_sha256'] and x['inspection_complete'] and any(r['bounds_xyxy']==[0,0,*dims] for r in regions)})
 reuse=d.get('completion',{}).get('reused_immutable_read_ledgers',[])
 if 'prior_complete_source_read_ledger' in d:reuse.append(d['prior_complete_source_read_ledger'])
 reused=[{'path':r['path'],'pass':h(Path(r['path']))==r['sha256']} for r in reuse]
 out.append({'ledger':name,'sha256':h(p),'texts':checks,'images':images,'reused_ledgers':reused,'all_passed':all(x['pass'] for x in checks+images+reused)})
result={'ledgers':out,'all_passed':all(x['all_passed'] for x in out),'note':'Validates exact declared complete delivery, native-image hashes/full bounds and immutable reuse chain. Old README delivered version is retained independently; current version also fully read. Underlying source10 full delivery independently validated in coverage-delivery-validation.json.'}
(B/'panel-delivery-validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'all_passed':result['all_passed'],'ledgers':[{k:(len(x[k]) if k in ['texts','images'] else x[k]) for k in ['ledger','texts','images','all_passed']} for x in out]}));assert result['all_passed']
