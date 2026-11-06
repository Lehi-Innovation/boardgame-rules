from pathlib import Path
import json,hashlib
from collections import defaultdict
from PIL import Image
B=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/spirit-island/2026-11-05-batch-002957');RP=B/'working-source-sweeps-43-44.json';LP=B/'working-source-sweeps-43-44-read-ledger.json';EXPECTED_R='6941666970200bef1f1419650372ea4f53f64cb4056229a6e20ec9310ade8664';EXPECTED_L='5770b97f4921dcd2219ab9ff7a2cfc25a2048dbe7efb7765ccdbc261a15b21f8';checks=[]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def canon(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def ck(v,n):
 checks.append({'name':n,'passed':bool(v)})
 if not v:raise AssertionError(n)
ck(sha(RP)==EXPECTED_R,'frozen original report hash');ck(sha(LP)==EXPECTED_L,'frozen original ledger hash');r=json.loads(RP.read_text());l=json.loads(LP.read_text());ck(r['read_ledger']['sha256']==sha(LP),'report exact ledger binding')
for i,a in enumerate(l['text_reads']):
 p=Path(a['path']);s=p.read_text();x,z=a['range'];ck(sha(p)==a['source_sha256'] and len(s)==a['character_length'],f'new text{i} exact file/length');ck(0<=x<z<=len(s) and z-x<=6000 and a['max_output_tokens']>=4000,f'new text{i} bounds/cap');ck(hashlib.sha256(s[x:z].encode()).hexdigest()==a['slice_utf8_sha256'],f'new text{i} slice hash');ck('no truncation' in a['actual_receipt_attestation'].lower() and 'truncation_check' in a,f'new text{i} explicit transport attestation fields')
for p in [B/'working-source-sweeps-43-44-prompt.txt',B/'working-pass-v21-supplement.json']:
 rr=sorted([a for a in l['text_reads'] if a['path']==str(p)],key=lambda a:a['range'][0]);cur=0
 for a in rr:ck(a['range'][0]==cur,'complete external input contiguous '+p.name);cur=a['range'][1]
 ck(cur==len(p.read_text()),'complete external input end '+p.name)
ck(len(l['text_reads'])==14 and not l['delivery_exceptions'],'all14 successful new deliveries; no failed delivery counted')
ledger_hashes={a['path']:a['sha256'] for a in l['immutable_reuse_bindings']}
for a in l['immutable_reuse_bindings']:ck(sha(a['path'])==a['sha256'],'immutable own ledger '+Path(a['path']).name)
for i,b in enumerate(l['complete_reused_text_source_bindings']):
 p=Path(b['path']);s=p.read_text();ck(sha(p)==b['sha256'] and len(s)==b['character_length'],f'complete reuse{i} original bytehash/length');rr=[]
 for ref in b['exact_original_row_indices']:
  path=ref['ledger'];ck(path in ledger_hashes and sha(path)==ledger_hashes[path],f'reuse{i} exact original ledger hash');a=json.loads(Path(path).read_text())['text_reads'][ref['index']];x,z=a['range'];ck(a['path']==str(p) and a.get('original_byte_sha256',a.get('source_sha256'))==b['sha256'],f'reuse{i} exact original row identity');ck(0<=x<z<=len(s) and z-x<=6000 and a['max_output_tokens']>=4000 and hashlib.sha256(s[x:z].encode()).hexdigest()==a.get('slice_utf8_sha256',a.get('slice_sha256')),f'reuse{i} original slice/cap/bounds');ck(('truncation_check' in a and 'no' in a['truncation_check'].lower()) or (a.get('truncated') is False and bool(a.get('delivery'))),f'reuse{i} explicit original successful-delivery/no-truncation fields');rr.append(a)
 cur=0
 for a in sorted(rr,key=lambda a:a['range'][0]):ck(a['range'][0]==cur,f'reuse{i} contiguous');cur=a['range'][1]
 ck(cur==len(s),f'reuse{i} complete model-delivered interval')
ck(len(l['complete_reused_text_source_bindings'])==17,'17 complete reused text bindings')
for i,a in enumerate(l['fresh_image_reads']):
 im=Image.open(a['path']);im.load();w,h=im.size;ck(sha(a['path'])==a['source_sha256'] and [w,h]==a['native_dimensions'] and a['full_view_bounds']==[0,0,w,h] and a['fully_viewed'],f'fresh image{i} hash/dimensions/fullframe attestation')
ck(len(l['fresh_image_reads'])==8,'all8 fresh backs')
original52=[]
for a in l['original_native_corpus_reuse']['source_ledgers']:
 ck(sha(a['path'])==a['sha256'],'original native ledger hash');original52+=json.loads(Path(a['path']).read_text())['image_reads']
ck(len(original52)==52 and canon(original52)==l['original_native_corpus_reuse']['prior_exact_rows_canonical_sha256'],'all52 original exact image rows canonical hash')
for i,a in enumerate(original52):
 im=Image.open(a['path']);im.load();w,h=im.size;v=a.get('viewed_region') or a['viewed_regions'][0]['bounds_xyxy'];ck(sha(a['path'])==a['original_byte_sha256'] and a.get('dimensions',a.get('native_dimensions'))==[w,h] and v==[0,0,w,h] and a.get('fully_viewed',a.get('inspection_complete')),f'original image{i} bytes/dimensions/fullbounds attestation')
a=l['recent_complete_native_view_reuse'];ck(sha(a['ledger'])==a['sha256'],'recent39 native-view ledger hash');prior=json.loads(Path(a['ledger']).read_text());recent=prior[a['field']];ck(len(recent)==39 and canon(recent)==a['row_canonical_sha256'] and a['row_indices']==list(range(39)),'exact39 reused native view rows')
for i,a in enumerate(recent):
 im=Image.open(a['path']);im.load();w,h=im.size;ck(sha(a['path'])==a['source_sha256'] and [w,h]==a['native_dimensions'] and a['viewed_region']==[0,0,w,h] and a['fully_viewed'],f'recent image{i} exact bytes/fullbounds')
a=l['native_provenance_metadata_reuse'];ck(sha(a['ledger'])==a['sha256'],'native metadata original ledger exact');n=json.loads(Path(a['ledger']).read_text());groups=defaultdict(list)
for i in a['text_row_indices']:
 t=n['text_reads'][i];p=Path(t.get('historical_original_preserved_at',t['path']));s=p.read_text();x,z=t['range'];ck(sha(p)==t['original_byte_sha256'] and len(s)==t['character_length'] and z-x<=6000 and t['max_output_tokens']>=4000 and hashlib.sha256(s[x:z].encode()).hexdigest()==t['slice_utf8_sha256'],f'native metadata row{i} actual version/cap/slice');groups[(t['path'],t['original_byte_sha256'],len(s))].append((x,z))
for key,rr in groups.items():
 cur=0
 for x,z in sorted(rr):ck(x==cur,'native metadata version contiguous');cur=z
 ck(cur==key[2],'native metadata full version complete')
packet=json.loads((B/'working-pass-v21-supplement.json').read_text());names=['questions.json','answer-key.json','asked-fact-map.json'];delta=['complete_new_question_objects','complete_new_key_objects','complete_new_asked_map_objects'];oldledger=json.loads((B/'working-source-sweeps-41-42-read-ledger.json').read_text())
for name,d in zip(names,delta):
 k='answers' if name=='answer-key.json' else 'questions';o=json.loads((B/'expanded-v20'/name).read_text())[k];v=json.loads((B/'expanded-v21'/name).read_text())[k];ck(sha(B/'expanded-v20'/name)==packet['prior171_equivalence']['prior_hashes'][name] and canon(o)==oldledger['current_bank_reconstruction'][name]['current171_canonical_sha256'],name+' exact own171 reconstruction binding');ck(len(o)==171 and len(v)==172 and v==o+packet[d] and sha(B/'expanded-v21'/name)==packet['full_bank_sha256'][name],name+' exact172 whole objects');ck(canon(v)==r['current_reconstruction_proof'][name]['reconstructed172_canonical_sha256'],name+' report canonical reconstruction')
q=json.loads((B/'expanded-v21/questions.json').read_text())['questions'];m=json.loads((B/'expanded-v21/asked-fact-map.json').read_text())['questions'];ck(sum(len(c['required_facts']) for v in m for c in v['requested_clauses'])==507,'507 actual required facts');ck(r['actual_question_IDs_compared']==[v['id'] for v in q],'172 IDs exact order');s='\n\n'.join(v['id']+' '+v['question']+'\nASKED: '+' | '.join(f for c in w['requested_clauses'] for f in c['required_facts']) for v,w in zip(q[:171],m[:171]))+'\n';ck(s==Path('/tmp/si41-actual-asks.txt').read_text() and sha('/tmp/si41-actual-asks.txt')=='562b87f60f2c8727e21a0928821ff44dccf439998fbd6683798f36c1d69033b7','old actual171 full model-delivered scratch preserved exactly')
# Scope files are never decoded: this is solely original/current byte identity against supplied packet hashes.
for version,hashes in [('expanded-v20',packet['prior171_equivalence']['prior_hashes']),('expanded-v21',packet['full_bank_sha256'])]:ck(sha(B/version/'core-scope-credit.json')==hashes['core-scope-credit.json'],version+' scope BYTE HASH ONLY')
for a in packet['new_primary_source_refs']:
 s=Path(a['file']).read_text();x,z=a['character_range'];ck(sha(a['file'])==a['file_sha256'] and hashlib.sha256(s[x:z].encode()).hexdigest()==a['passage_sha256'],'Q172 exact primary source/range hash')
ck([p['pass_number'] for p in r['passes']]==[43,44] and [p['new_question_count'] for p in r['passes']]==[0,0] and all(p['complete_remaining_gaps']==[] for p in r['passes']),'both actual pass results0/0 recorded; not a semantic/global-coverage proof');ck(not r['global_fresh_independent_PASS'] and r['questions_added']==0,'no global verdict or bank additions')
ck(sha(B/'working-source-sweeps-41-42.json')=='6076b487c91cf82f9935493d688668be384c44b206497854297587467b276c1c' and sha(B/'working-source-sweeps-41-42-read-ledger.json')=='1d64e6cbbbcdb9a009518775286a618243fd7fd9a92cf5a6d6c9648f7e96addc','old41/42 artifacts preserved');ck(sha(RP)==EXPECTED_R and sha(LP)==EXPECTED_L,'original43/44 artifacts unchanged after validation')
out={'status':'PASS for evidence checks only','passed_checks':len(checks),'failed_checks':0,'report':{'path':str(RP),'sha256':sha(RP)},'ledger':{'path':str(LP),'sha256':sha(LP)},'helper':{'path':str(Path(__file__).resolve()),'sha256':sha(__file__)},'counts':{'new_text_rows':14,'fresh_image_views':8,'complete_reused_text_bindings':17,'immutable_reuse_ledgers':7,'original_image_rows':52,'recent_native_view_rows':39,'questions':172,'required_facts':507,'recorded_new_question_counts':[0,0]},'delivery_exceptions':[],'validator_development_exception':{'initial_helper_path':'/tmp/si43-delivery-validator-schema-assumption-initial.py','initial_helper_sha256':sha('/tmp/si43-delivery-validator-schema-assumption-initial.py'),'reason':'Initial validator expected the older truncation_check string in every reuse row. Own41/42 rows instead explicitly use truncated:false plus delivery text. Corrected the helper to validate both original schema forms without changing either original artifact or any evidence row. No source delivery was missing or newly inferred.'},'machine_vs_attestation':'Machine checks establish exact bytes, source/slice hashes, contiguous range coverage, caps, object equality, image decode/dimensions/fullbounds. Model receipt/no transport truncation and visual reading remain explicit attestations in original rows. Scope files are byte-hash-only. No semantic completeness or global coverage verdict.','checks':checks};proof=Path('/tmp/si43-delivery-validation.json');proof.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'passed_checks':len(checks),'failed_checks':0,'report_sha256':sha(RP),'ledger_sha256':sha(LP),'helper_sha256':sha(__file__),'proof_sha256':sha(proof),'proof_path':str(proof)},indent=2))
