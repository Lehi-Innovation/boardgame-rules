from pathlib import Path
import json,hashlib
from PIL import Image
B=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/spirit-island/2026-11-05-batch-002957');R=B/'working-source-sweeps-41-42.json';L=B/'working-source-sweeps-41-42-read-ledger.json';r=json.loads(R.read_text());l=json.loads(L.read_text());checks=[]
def ck(x,n):
 checks.append({'check':n,'pass':bool(x)});assert x,n
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
ck(r['read_ledger']['sha256']==sha(L),'report binds exact ledger hash')
for i,a in enumerate(l['text_reads']):
 p=Path(a['path']);s=p.read_text();x,z=a['range'];ck(sha(p)==a['source_sha256'] and len(s)==a['source_character_count'],f'text{i} source bytes and length');ck(0<=x<z<=len(s) and z-x<=6000 and a['max_output_tokens']>=4000 and not a['truncated'],f'text{i} bounds cap observer no-truncation');ck(hashlib.sha256(s[x:z].encode()).hexdigest()==a['slice_sha256'],f'text{i} slice hash')
for p in [str(B/'working-source-sweeps-41-42-prompt.txt'),str(B/'working-pass-v20-supplement.json'),'/tmp/si41-actual-asks.txt',str(B/'scope-and-coverage-10-prompt.txt')]:
 rows=sorted([x for x in l['text_reads'] if x['path']==p],key=lambda x:x['range'][0]);cursor=0
 for a in rows:ck(a['range'][0]==cursor,'complete input contiguous '+Path(p).name);cursor=a['range'][1]
 ck(cursor==len(Path(p).read_text()),'complete input end '+Path(p).name)
for a in l['immutable_reuse_bindings']:ck(sha(a['path'])==a['sha256'],'immutable reuse ledger '+Path(a['path']).name)
for b in l['complete_reused_text_source_bindings']:
 s=Path(b['path']).read_text();ck(sha(b['path'])==b['sha256'],'reuse source '+Path(b['path']).name);rows=[]
 for ref in b['exact_original_row_indices']:
  original=json.loads(Path(ref['ledger']).read_text())['text_reads'][ref['index']];rows.append(original);a,z=original['range'];ck(original['max_output_tokens']>=4000 and z-a<=6000 and hashlib.sha256(s[a:z].encode()).hexdigest()==original.get('slice_utf8_sha256',original.get('slice_sha256')),'reuse row '+str(ref['index']))
 cursor=0
 for a in sorted(rows,key=lambda x:x['range'][0]):ck(a['range'][0]==cursor,'reuse contiguous '+Path(b['path']).name);cursor=a['range'][1]
 ck(cursor==len(s),'reuse complete '+Path(b['path']).name)
for i,a in enumerate(l['fresh_native_image_reads']):
 im=Image.open(a['path']);im.load();w,h=im.size;ck(sha(a['path'])==a['source_sha256'] and [w,h]==a['native_dimensions'] and a['viewed_region']==[0,0,w,h] and a['fully_viewed'],f'freshimage{i}hash dimensions/fullbounds attestation')
original52=[]
for a in l['reused_original_image_corpus']['source_ledgers']:
 ck(sha(a['path'])==a['sha256'],'original image ledger');original52+=json.loads(Path(a['path']).read_text())['image_reads']
ck(hashlib.sha256(json.dumps(original52,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()==l['reused_original_image_corpus']['prior_exact_rows_canonical_sha256'],'original52 exact row canonical hash')
for i,a in enumerate(original52):
 im=Image.open(a['path']);im.load();w,h=im.size;bounds=a.get('viewed_region');bounds=bounds if bounds else a['viewed_regions'][0]['bounds_xyxy'];ck(sha(a['path'])==a['original_byte_sha256'] and [w,h]==a.get('dimensions',a.get('native_dimensions')) and bounds==[0,0,w,h],f'reusedimage{i} hash dimensions fullbounds')
# Verify preserved native metadata versions by complete groups, including old README snapshot.
native=json.loads((B/'original-panel-audit-01-read-ledger.json').read_text());groups={}
for i,a in enumerate(native['text_reads']):
 p=Path(a.get('historical_original_preserved_at',a['path']));s=p.read_text();x,z=a['range'];ck(sha(p)==a['original_byte_sha256'] and len(s)==a['character_length'] and a['max_output_tokens']>=4000 and z-x<=6000 and hashlib.sha256(s[x:z].encode()).hexdigest()==a['slice_utf8_sha256'],f'native metadata row{i}');groups.setdefault((a['path'],a['original_byte_sha256'],len(s)),[]).append(a['range'])
for (p,h,n),rows in groups.items():
 cursor=0
 for a,z in sorted(rows):ck(a==cursor,'native metadata version contiguous');cursor=z
 ck(cursor==n,'native metadata version complete')
p=json.loads((B/'working-pass-v20-supplement.json').read_text());names=['questions.json','answer-key.json','asked-fact-map.json'];deltas=['complete_new_question_objects','complete_new_key_objects','complete_new_asked_map_objects']
for name,delta in zip(names,deltas):
 k='answers' if name=='answer-key.json' else 'questions';old=json.loads((B/'expanded-v19'/name).read_text())[k];new=json.loads((B/'expanded-v20'/name).read_text())[k];ck(sha(B/'expanded-v20'/name)==p['full_bank_sha256'][name] and len(new)==171 and new==old+p[delta],name+' exact171 reconstruction');ck(len(old)==170 and sha(B/'expanded-v19'/name)==p['prior170_equivalence']['prior_hashes'][name],name+' exact unchanged prior170')
q=json.loads((B/'expanded-v20/questions.json').read_text())['questions'];m=json.loads((B/'expanded-v20/asked-fact-map.json').read_text())['questions'];ck(sum(len(c['required_facts']) for x in m for c in x['requested_clauses'])==506,'exact506 asked facts');ck(r['actual_ask_IDs_compared']==[x['id'] for x in q],'171 IDs exactorder');projection='\n\n'.join(x['id']+' '+x['question']+'\nASKED: '+' | '.join(f for c in y['requested_clauses'] for f in c['required_facts']) for x,y in zip(q,m))+'\n';ck(projection==Path('/tmp/si41-actual-asks.txt').read_text(),'fresh actual-ask projection exact literal strings')
ck([p['pass_number'] for p in r['passes']]==[41,42] and [p['new_question_count'] for p in r['passes']]==[1,0] and [len(p['complete_remaining_gaps']) for p in r['passes']]==[1,0],'recorded actual pass results1/0, not a semantic completeness proof');ck(not r['global_fresh_independent_PASS'] and r['questions_added_to_bank']==0,'no global PASS/bank additions')
gap=r['passes'][0]['complete_remaining_gaps'][0];src=gap['primary_sources'][0];s=Path(src['path']).read_text();a,z=src['character_range'];ck(sha(src['path'])==src['sha256'] and hashlib.sha256(s[a:z].encode()).hexdigest()==src['passage_sha256'] and gap['primary_passage']==s[a:z],'retained permission exact primary passage')
ck(sha(B/'working-source-sweeps-39-40.json')=='428e4f5fe301869c7419deadfda9cb9da4f6125cca698be88ba8764dc1fdeda3' and sha(B/'working-source-sweeps-39-40-read-ledger.json')=='7ed3821cb67400a7f5faccd8f2f7da626275a90019f122b80e3c4a672bf9c25f','prior raw39/40 artifacts preserved');ck(sha(B/'expanded-v20/core-scope-credit.json')==p['full_bank_sha256']['core-scope-credit.json'],'scope-credit BYTE HASH ONLY')
out={'passed':len(checks),'failed':0,'report_sha256':sha(R),'ledger_sha256':sha(L),'checks':checks,'limits':'Bytes, object equality, bounds and caps are machine checked. Model receipt, transport no-truncation and visual reading remain attestations; no global coverage verdict.'};Path('/tmp/si41-validation.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2))
