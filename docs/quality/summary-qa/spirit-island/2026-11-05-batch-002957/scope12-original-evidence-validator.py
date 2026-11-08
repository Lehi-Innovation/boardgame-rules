#!/usr/bin/env python3
"""Read-only frozen review12 object validator; creates only unique /tmp evidence."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, collections, shutil
from PIL import Image
from bs4 import BeautifulSoup
B=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/spirit-island/2026-11-05-batch-002957')
P=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/batches/2026-11-05-batch-002957/source-preflight/spirit-island')
TOKEN='694aaff2dd604dc4b5a216a740b761bd'
OUT=Path('/tmp/scope12-evidence-proof-'+TOKEN+'.json')
COPY=Path('/tmp/scope12-frozen-preservation-'+TOKEN)
assert not OUT.exists() and not COPY.exists(), 'Refuse overwrite'
COPY.mkdir(mode=0o700)
hashof=lambda b:hashlib.sha256(b).hexdigest()
opened={}; checks=[]; failures=[]
def readbytes(p):
 p=Path(p);raw=p.read_bytes();opened[str(p)]=hashof(raw);return raw
def obj(p):return json.loads(readbytes(p).decode('utf-8'))
def check(label,ok,details=None):
 row={'check':label,'ok':bool(ok)}
 if details is not None:row['details']=details
 checks.append(row)
 if not ok:failures.append(row)
def copy_original(p,raw=None):
 p=Path(p);raw=readbytes(p)if raw is None else raw
 dest=COPY/(str(len(preserved)).zfill(3)+'-'+p.name)
 with dest.open('xb')as f:f.write(raw)
 h=hashof(raw);check('preservation copy '+str(p),hashof(dest.read_bytes())==h)
 preserved.append({'original_path':str(p),'preserved_path':str(dest),'sha256':h,'bytes':len(raw)})
preserved=[]
expected_artifacts={
 'scope-coverage-12-read-ledger.json':'0912aa42e2ad7f3550d430dc760ff1016b156d61b056a6f365439022a44f4928',
 'question-key-scope-review-12.json':'3338e0688c250dc1776c7398ff3499d1ef1a598ff038048385950f8570521560',
 'coverage-review-12.json':'bd668e98359e76e32552ef8d7fb099fd70abaf8de37f43d61c72aaec40c3d272'}
artifacts={}
for name,want in expected_artifacts.items():
 raw=readbytes(B/name);check('frozen artifact exact hash '+name,hashof(raw)==want,{'expected':want,'actual':hashof(raw)});copy_original(B/name,raw);artifacts[name]=json.loads(raw)
L=artifacts['scope-coverage-12-read-ledger.json'];R=artifacts['question-key-scope-review-12.json'];C=artifacts['coverage-review-12.json']
original_expected={str(B/x)for x in ['coverage-review-12-input-manifest.json','source-manifest.json','scope-reachability-steering-2026-11-05.txt','supplemental-source-manifest-v4.json','card-scope-source/what-do-range-boosts-affect.txt','card-scope-source/range-in-text-of-powers-that-target-spirits.txt','card-scope-source/core-second-printing.txt','novelty11-source-scratch/novelty11-publisher-updates.txt','expanded-v21/questions.json','expanded-v21/answer-key.json','expanded-v21/asked-fact-map.json','expanded-v21/core-scope-credit.json','coverage-map-for-review-12.json','scope-and-coverage-12-prompt.txt']}
original_expected.update(str(P/x)for x in ['living-faq-core-game.txt','living-faq-setup.txt','original-spirit-panels/README.md','original-spirit-panels/panel-download-map.json','original-spirit-panels/download-integrity.json','original-spirit-panels/independent-printed-photo-corroboration.json'])
original_expected.update(['/home/jonny/projects/boardgame-rules/extracted/spirit-island-rules.txt','/tmp/scope12-publisher-branch-claw-visible.txt'])
comparison_expected={'/tmp/scope12-literal-ask-fact-comparison.txt','/tmp/scope12-noncredit-clauses.txt'}
check('exact 24 text paths',set(L['text_inputs'])==original_expected|comparison_expected,{'original_count':len(original_expected),'comparison_count':len(comparison_expected),'actual_count':len(L['text_inputs'])})
text_proof=[];slice_count=0
for path,v in L['text_inputs'].items():
 raw=readbytes(path);text=raw.decode('utf-8');copy_original(path,raw);pos=0;proof=[]
 check('full text bytes/characters/hash '+path,v['path']==path and v['full_byte_sha256']==hashof(raw)and v['byte_length']==len(raw)and v['character_length']==len(text))
 for i,z in enumerate(v['slices']):
  a,b=z['start'],z['end'];h=hashof(text[a:b].encode('utf-8'))
  valid=(isinstance(a,int)and isinstance(b,int)and a==pos and a<b<=len(text)and b-a<=6000 and z['character_cap']<=6000 and z['character_cap']>=b-a and z['max_output_tokens']>=4000 and z['truncated']is False and z['received']is True and z['utf8_sha256']==h)
  check('slice object '+path+' #'+str(i),valid)
  proof.append({'index':i,'start':a,'end':b,'utf8_sha256':h,'recorded_cap':z['character_cap'],'recorded_output_token_cap':z['max_output_tokens'],'recorded_truncated':z['truncated'],'recorded_received':z['received']});pos=b;slice_count+=1
 check('full contiguous coverage '+path,pos==len(text)and v['slices'][0]['start']==0)
 text_proof.append({'path':path,'full_byte_sha256':hashof(raw),'byte_length':len(raw),'character_length':len(text),'slice_count':len(proof),'slices':proof})
check('exact229 slice objects',slice_count==229,{'actual':slice_count})
check('ledger delivery declarations agree with machine counts',L['delivery_verification']['total_text_inputs']==24 and L['delivery_verification']['total_slices']==229 and L['delivery_verification']['full_image_inputs']==54 and L['delivery_verification']['unrecovered_truncations']==0)
Q=obj(B/'expanded-v21/questions.json')['questions'];K=obj(B/'expanded-v21/answer-key.json')['answers'];M=obj(B/'expanded-v21/asked-fact-map.json');S=obj(B/'expanded-v21/core-scope-credit.json')
comparison='\n'.join(x['id']+' '+x['question']+'\n  '+'\n  '.join(f for c in x['requested_clauses']for f in c['required_facts'])for x in M['questions'])
noncredit='\n'.join(x['id']+' '+x.get('scope_result','')+' '+json.dumps(x.get('noncredited_clauses'),ensure_ascii=False)for x in S['questions']if x.get('scope_result')!='base_supported')
check('comparison derivative exact reproducibility',readbytes('/tmp/scope12-literal-ask-fact-comparison.txt')==comparison.encode('utf-8'))
check('noncredit derivative exact reproducibility',readbytes('/tmp/scope12-noncredit-clauses.txt')==noncredit.encode('utf-8'))
check('diagnostic truncation recovery recorded and whole four-slice derivative present',bool(L['delivery_verification']['ancillary_truncation_recovery'])and len(L['text_inputs']['/tmp/scope12-noncredit-clauses.txt']['slices'])==4)
derivation_proof=[]
for d in L['derivations']:
 raw=readbytes(d['source_path']);copy_original(d['source_path'],raw);soup=BeautifulSoup(raw.decode('utf-8'),'html.parser')
 for n in soup(['script','style','noscript']):n.decompose()
 visible=soup.get_text('\n',strip=True).encode('utf-8');actual=readbytes(d['output_path'])
 check('publisher HTML derivative original hash and exact reproduction',hashof(raw)==d['original_html_sha256']and visible==actual and hashof(actual)==d['output_sha256']and len(actual.decode())==d['character_length'])
 derivation_proof.append(dict(d,exact_visible_prose_reproduction=True))
spirits=['lightning','river','earth','shadows','green','thunderspeaker','ocean','bringer']
panels={f'{s}-{face}.png'for s in spirits for face in ['front','back']}
identity={'corroborating-all-spirits-2017.jpg','corroborating-river-2018.jpg','corroborating-2017-bringer-track-crop.png','branch-claw-rulebook-p6.png','all-named-card-title-corner-strips.jpg'}
image_proof=[];seen_names=[]
for v in L['images']:
 path=v['path'];raw=readbytes(path);copy_original(path,raw);name=Path(path).name;seen_names.append(name)
 with Image.open(path)as im:fmt=im.format;dims=list(im.size);im.verify()
 with Image.open(path)as im:im.load()
 category='original_native_panel'if name in panels else'membership_or_photo_identity'if name in identity else'card_face'
 check('image bytes/decode/recorded whole-view '+name,hashof(raw)==v['sha256']and v['fully_viewed']is True and v['view_detail']=='original'and bool(v['regions'])and bool(v['observations']))
 if category=='original_native_panel':check('native panel whole-face/region record '+name,'whole image'in v['regions']and dims==[2697,1797])
 image_proof.append({'path':path,'sha256':hashof(raw),'bytes':len(raw),'format':fmt,'pixel_dimensions':dims,'category':category,'recorded_full_view':v['fully_viewed'],'recorded_detail':v['view_detail'],'recorded_regions':v['regions'],'recorded_observations':v['observations'],'historical_perception_machine_proven':False})
check('exact54 unique image objects',len(image_proof)==len(set(seen_names))==54)
check('all16 native original panel identities present',panels<=set(seen_names)and sum(x['category']=='original_native_panel'for x in image_proof)==16)
check('all5 membership/photo identity records present',identity<=set(seen_names)and sum(x['category']=='membership_or_photo_identity'for x in image_proof)==5)
cardrows=C['complete_corpus_challenge']['card_face_challenge'];panelrows=C['complete_corpus_challenge']['native_original_panel_challenge']
check('coverage card count31core2excluded',len(cardrows)==33 and collections.Counter(x['membership']for x in cardrows)=={'original_core':31,'excluded_Branch_and_Claw':2})
check('excluded example identities',set(Path(x['path']).name for x in cardrows if x['membership']=='excluded_Branch_and_Claw')=={'sky_stretches_to_shore.jpg','cast_down_into_the_briny_deep.jpg'})
byimage={x['path']:x for x in L['images']}
check('report33card16panel records agree exactly with ledger image hashes and view flags',len(panelrows)==16 and all(x['path']in byimage and x['sha256']==byimage[x['path']]['sha256']and x['fully_viewed']==byimage[x['path']]['fully_viewed']for x in cardrows+panelrows))
expected_ids=[f'Q{i:02}'for i in range(1,173)]
for label,rows in [('questions',Q),('keys',K),('map',M['questions']),('scope',S['questions']),('report scope_validation',R['scope_validation']),('report question_checks',R['question_checks'])]:check('172 ordered IDs '+label,[x['id']for x in rows]==expected_ids)
for label,r in [('keyscope',R),('coverage',C)]:check('report172IDs507facts '+label,r['checked_question_ids']==expected_ids and r['checked_question_count']==172 and r['checked_required_fact_count']==507 and r['asked_fact_map_sha256']==hashof(readbytes(B/'expanded-v21/asked-fact-map.json')))
fact_map=[]
for qi,x in enumerate(M['questions']):
 check('map literal question identity '+x['id'],x['question']==Q[qi]['question'])
 for ci,c in enumerate(x['requested_clauses']):
  for fi,f in enumerate(c['required_facts']):fact_map.append({'fact_index':len(fact_map),'question_id':x['id'],'question_index':qi,'clause_index':ci,'clause_id':c['clause_id'],'required_fact_index_in_clause':fi,'json_pointer':f'/questions/{qi}/requested_clauses/{ci}/required_facts/{fi}','required_fact':f,'required_fact_utf8_sha256':hashof(f.encode('utf-8'))})
check('507 derived fact_index mappings form exact bijection',len(fact_map)==M['required_fact_count']==507 and[x['fact_index']for x in fact_map]==list(range(507))and len({x['json_pointer']for x in fact_map})==507)
common=set(R)&set(C)
check('all common report fields agree exactly',all(R[k]==C[k]for k in common),{'shared_fields':sorted(common)})
expected_inputhash={p:v['full_byte_sha256']for p,v in L['text_inputs'].items()};expected_inputhash.update({x['path']:x['sha256']for x in L['images']});expected_inputhash.update({d['source_path']:d['original_html_sha256']for d in L['derivations']})
check('both reports exact79 input hashes agree with ledger',R['input_hashes']==C['input_hashes']==expected_inputhash and len(expected_inputhash)==79)
for path,want in expected_inputhash.items():check('frozen current input hash '+path,hashof(readbytes(path))==want)
for path,want in obj(B/'coverage-review-12-input-manifest.json')['sha256'].items():check('frozen manifest hash '+path,path in expected_inputhash and hashof(readbytes(path))==want)
ledgerhash=expected_artifacts['scope-coverage-12-read-ledger.json']
for label,r in [('keyscope',R),('coverage',C)]:check('ledger linkage '+label,r['read_evidence']=={'ledger_path':str(B/'scope-coverage-12-read-ledger.json'),'sha256':ledgerhash,'complete':True})
findings=R['asked_fact_mapping_findings'];check('original exactly2 complete MAP findings',[x['finding_id']for x in findings]==['MAP12-01','MAP12-02']and[x['question_id']for x in findings]==['Q09','Q65']and findings==C['asked_fact_mapping_findings'])
for finding in findings:
 current=M
 for part in finding['json_pointer'].split('/')[1:]:current=current[int(part)]if isinstance(current,list)else current[part]
 check('MAP exact old fact pointer '+finding['finding_id'],current==finding['exact_old_text']and bool(finding['correction'])and bool(finding['reason'])and bool(finding['primary_sources'])and finding['fixed_key_change_needed']is False)
 for z in finding['primary_sources']:
  raw=readbytes(z['path']);text=raw.decode();a,b=z['character_range'];check('MAP exact primary passage '+finding['finding_id'],hashof(raw)==z['file_sha256']and text[a:b]==z['exact_passage']and hashof(text[a:b].encode())==z['passage_utf8_sha256'])
check('original outcome retained without new semantic verdict',R['verdict']==C['verdict']=='FAIL'and R['fixed_key_verdict']==C['fixed_key_verdict']=='PASS'and R['asked_fact_mapping_verdict']==C['asked_fact_mapping_verdict']=='FAIL'and C['coverage_verdict']=='PASS'and C['stopping_verdict']=='FAIL'and C['remaining_gap_count']==0 and C['remaining_gaps']==[]and C['unresolved_stopping_findings']==['MAP12-01','MAP12-02'])
check('zero original key/missing/scope findings',all(R[k]==C[k]==[]for k in ['fixed_key_findings','missing_truly_asked_facts_in_map','missing_truly_asked_facts_in_fixed_key','scope_findings']))
check('question-level mapping statuses agree with findings',[x['id']for x in R['question_checks']if x['asked_fact_mapping']=='FAIL']==['Q09','Q65']and all(x['fixed_key']=='PASS'for x in R['question_checks']))
# Preserve known existing review12 scratch without executing or editing it.
for name in ['scope12-read.py','scope12-read-ledger.json','scope12-record-images.py','scope12-card-paths.json','scope12-text-meta.json','scope12-write-reports.py']:
 p=Path('/tmp')/name
 if p.exists():copy_original(p)
for path,want in dict(opened).items():check('post-validation bytes preserved '+path,hashof(Path(path).read_bytes())==want)
for name,want in expected_artifacts.items():check('frozen output exact hash unchanged at end '+name,hashof((B/name).read_bytes())==want)
script=Path(__file__).resolve()
proof={'purpose':'Evidence validation only; original semantic review and its FAIL outcome remain frozen. No repair and no new semantic verdict.','validator_path':str(script),'validator_sha256':hashof(script.read_bytes()),'created_utc':datetime.now(timezone.utc).isoformat(),'filesystem_object_validation':{'all_checks_passed':not failures,'check_count':len(checks),'failures':failures,'checks':checks,'frozen_original_artifact_hashes':expected_artifacts,'text_inputs':text_proof,'derived_507_fact_index_mappings':fact_map,'fact_index_note':'The frozen asked-fact-map stores required_facts in ordered nested arrays and has no explicit fact_index field. These zero-based0..506 indices are validation-derived identities, not newly claimed original fields or changed rubric facts.','images':image_proof,'publisher_prose_derivation':derivation_proof,'opened_original_paths_and_sha256':opened,'preservation_copies':preserved},'historical_receipt_and_perception_attestations':{'machine_proof_limit':'Filesystem equality, parsed object fields, Unicode slice recomputation, derivative reproducibility and image decoding do not independently prove historical tool-response delivery, historical output caps, actual reading, full visual perception or printed membership recognition. No transcript/runtime or peer/parent report was inspected.','reviewer_attestation':'As the original reviewer, I attest that the listed text slices were actually received/read and the images actually viewed during the original review. The ledger records those assertions, including the recovered diagnostic truncation. This validation does not re-perceive images or issue a fresh semantic opinion.','ledger_independence':L['independence'],'ledger_native_visual_read_note':L['native_visual_read_note'],'ledger_truncation_recovery':L['delivery_verification']['ancillary_truncation_recovery'],'recorded_24_input_229_slice_54_image_counts':[24,229,54],'receipt_claims_are_attestations':True,'visual_membership_claims_are_attestations':True,'current_machine_validation_claims_are_separate':True},'unchanged_original_outcome':{'fixed_key_verdict':R['fixed_key_verdict'],'asked_fact_mapping_verdict':R['asked_fact_mapping_verdict'],'coverage_verdict':C['coverage_verdict'],'stopping_verdict':C['stopping_verdict'],'top_level_verdict':C['verdict'],'map_finding_ids':[x['finding_id']for x in findings],'remaining_procedure_gaps':C['remaining_gap_count']}}
with OUT.open('x',encoding='utf-8')as f:json.dump(proof,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps({'validator':str(script),'validator_sha256':hashof(script.read_bytes()),'proof':str(OUT),'proof_sha256':hashof(OUT.read_bytes()),'preservation_directory':str(COPY),'all_checks_passed':not failures,'checks':len(checks),'failures':failures,'facts':len(fact_map),'texts':len(text_proof),'slices':slice_count,'images':len(image_proof)},ensure_ascii=False))
raise SystemExit(0 if not failures else 1)
