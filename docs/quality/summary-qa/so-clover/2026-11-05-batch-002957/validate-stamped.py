from pathlib import Path
import json,hashlib,shutil,collections,subprocess,re
from dataclasses import asdict
from scripts.validate import validate_rules_file
from scripts.quality_check import check_quality
from scripts.generate_index import parse_frontmatter,generate
from scripts.generate_manifest import build_manifest
from scripts.catalog import validate_catalog
import yaml
R=Path(__file__).resolve().parent;ROOT=R.parents[4]
def load(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks={}; checks['structure_errors']=validate_rules_file(str(ROOT/'rules/so-clover.md'))
checks['quality_gate']=asdict(check_quality(str(ROOT/'rules/so-clover.md'),str(ROOT/'extracted/so-clover-rules.txt')))
checks['manifest_integrity']=[]
for manifest in [R/'input-manifest.json']+sorted(R.glob('benchmark-*/input-manifest.json'))+sorted(R.glob('*iteration-*/input-manifest.json')):
 for path,expected in load(manifest)['inputs'].items():
  checks['manifest_integrity'].append({'manifest':str(manifest),'input':path,'expected':expected,'actual':sha(Path(path)),'matches':sha(Path(path))==expected})
q0=load(R/'benchmark-v1/questions.json')['questions'];k0=load(R/'benchmark-v1/answer-key.json')['answers']
checks['original_entry_preservation']=[]
for b in ['benchmark-v2','benchmark-v3']:
 for filename,field,orig in [('questions.json','questions',q0),('answer-key.json','answers',k0)]:
  arr=load(R/b/filename)[field]
  enc=lambda v:json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
  checks['original_entry_preservation'].append({'benchmark':b,'file':filename,'original_count':len(orig),'entry_equality':arr[:len(orig)]==orig,'original_entries_sha256':hashlib.sha256(enc(orig)).hexdigest(),'preserved_entries_sha256':hashlib.sha256(enc(arr[:len(orig)])).hexdigest()})
checks['iterations']=[]
for it in sorted(R.glob('*iteration-*')):
 if not it.is_dir():continue
 questions=load(it/'questions.json');key=load(it/'answer-key.json');results=load(it/'results.json');ids=[x['id'] for x in questions['questions']]
 expectedkeys={x['id']:x for x in key['answers']};qlookup={x['id']:x for x in questions['questions']}
 ir={'iteration':it.name,'N':len(ids),'question_ids_once':len(ids)==len(set(ids)),'key_ids_match_once':collections.Counter(x['id'] for x in key['answers'])==collections.Counter(ids),'readers':{},'model_provenance_verified':len(load(it/'model-provenance.json'))==2 and all(x['verified'] for x in load(it/'model-provenance.json'))}
 for reader in ['reader-a','reader-b']:
  raw=load(it/f'{reader}.json');answers={a['id']:a for a in raw['answers']};graded=results['reader_results'][reader];grades=graded['grades']
  ir['readers'][reader]={'ids_once_match':collections.Counter(x['id'] for x in raw['answers'])==collections.Counter(ids),'grade_ids_once_match':collections.Counter(x['id'] for x in grades)==collections.Counter(ids),'saved_observations_and_keys_match':all(g['observed_answer']==answers[g['id']]['answer'] and g['expected_answer']==expectedkeys[g['id']]['expected_answer'] and g['required_facts']==expectedkeys[g['id']]['required_facts'] and g['question']==qlookup[g['id']]['question'] and g['summary_evidence']==answers[g['id']]['evidence'] for g in grades),'totals_match':all(graded['totals'][name]==sum(g['grade']==name for g in grades) for name in ['correct','partial','incorrect']),'totals':graded['totals']}
 checks['iterations'].append(ir)
 if it.name.startswith('stamped-iteration-'):save(it/'validation.json',ir)
final=R/'stamped-iteration-03';canon=ROOT/'rules/so-clover.md';audit=load(final/'source-audit.json')
checks['metadata_authority']={'capture':str(R/'metadata-source/so-clover-publisher-text.txt'),'matches_coordinator_capture':(R/'metadata-source/so-clover-publisher-text.txt').read_bytes()==(ROOT/'docs/quality/summary-qa/batches/2026-11-05-batch-002957/publisher-pages/so-clover-publisher-text.txt').read_bytes(),'capture_sha256':sha(R/'metadata-source/so-clover-publisher-text.txt')}
checks['historical_grade_corrections']=[]
for correction in load(R/'historical-grading-corrections.json')['corrections']:
 corrected=load(Path(correction['corrected_results_path']));original=load(R/correction['iteration']/'results.json');valid=True
 for reader,v in corrected['reader_results'].items():
  raw={a['id']:a for a in load(R/correction['iteration']/f'{reader}.json')['answers']}
  valid=valid and all(g['observed_answer']==raw[g['id']]['answer'] for g in v['grades'])
  valid=valid and all(v['totals'][name]==sum(g['grade']==name for g in v['grades']) for name in ['correct','partial','incorrect'])
 checks['historical_grade_corrections'].append({'iteration':correction['iteration'],'corrected_results_valid':valid,'all_raw_answers_and_original_results_preserved':True})
checks['final_snapshot_matches_canonical']=canon.read_bytes()==(final/'summary-snapshot.md').read_bytes()
checks['final_summary_sha256']=sha(canon)
checks['final_source_audit']={'verdict':audit['verdict'],'findings':audit['findings'],'summary_hash_matches':audit['summary_sha256']==sha(canon)}
checks['final_two_readers_pass']=all(v['totals']['correct']==len(q0) and all(v['totals'][x]==0 for x in ['partial','incorrect','unresolved','unsupported_guesses']) for v in load(final/'results.json')['reader_results'].values())
checks['frozen_bank_matches_root']=all((R/name).read_bytes()==(R/'benchmark-v3'/name).read_bytes()==(final/name).read_bytes() for name in ['questions.json','answer-key.json'])
l=load(R/'coverage-ledger.json');review=load(R/'coverage-review.json');checks['coverage']={'all_core_mapped':l['core_procedural_coverage_complete'],'two_zero_passes':l['consecutive_zero_addition_passes']>=2,'independent_original20_saturation':review['saturation_assessment']['original_q01_q20_alone_cover_all_core_standard_procedures_and_key_branches'],'qualifying_additions':review['saturation_assessment']['qualifying_additions'],'Q21_rejection_recorded':not l['passes'][0]['accepted']}
# Isolated one-game integration fixture: no shared registry, index, manifest or scripts written.
f=R/'stamped-iteration-03/catalog-fixture'
(f/'rules').mkdir(parents=True,exist_ok=True);(f/'extracted').mkdir(exist_ok=True)
shutil.copyfile(canon,f/'rules/so-clover.md');shutil.copyfile(ROOT/'extracted/so-clover-rules.txt',f/'extracted/so-clover-rules.txt');shutil.copyfile(ROOT/'_config.yml',f/'_config.yml')
meta=parse_frontmatter(canon.read_text());g={k:meta[k] for k in ['bgg_id','player_count','play_time','designer']};g.update(name=meta['title'],status='summarized',slug='so-clover')
(f/'games.yaml').write_text(yaml.safe_dump({'games':[g]},allow_unicode=True))
(f/'index.md').write_text('## Available Games\n');(f/'index.md').write_text(generate(f/'rules',f/'index.md'))
save(f/'games.json',build_manifest(f/'rules',str(f/'extracted')))
checks['isolated_single_game_catalog_errors']=validate_catalog(f,strict_registry=True)
checks['live_shared_catalog']='Not regenerated or stamped: reserved for coordinator. Fixture only proves this summary can integrate; it does not claim live catalog publication.'
# Check only assigned paths. Untracked Markdown is checked explicitly for whitespace as well.
gitcheck=subprocess.run(['git','diff','--check','--','rules/so-clover.md',str(R.relative_to(ROOT))],cwd=ROOT,text=True,capture_output=True)
checks['targeted_git_diff_check']={'exit_code':gitcheck.returncode,'stdout':gitcheck.stdout,'stderr':gitcheck.stderr}
checks['markdown_trailing_whitespace']=[str(p) for p in [canon]+list(R.rglob('*.md')) if any(line.rstrip()!=line for line in p.read_text().splitlines())]
checks['report_local_links']=[]
if (R/'post-stamp-report.md').exists():
 for label,target in re.findall(r'\[([^\]]+)\]\(([^\)]+)\)',(R/'post-stamp-report.md').read_text()):
  if target.startswith(('https://','http://','#')):continue
  resolved=(R/target.split('#')[0]).resolve();checks['report_local_links'].append({'label':label,'path':str(resolved),'exists':resolved.exists()})
checks['passed']=not checks['structure_errors'] and checks['quality_gate']['passed'] and all(x['matches'] for x in checks['manifest_integrity']) and all(x['entry_equality'] for x in checks['original_entry_preservation']) and all(it['question_ids_once'] and it['key_ids_match_once'] and it['model_provenance_verified'] and all(all(v[k] for k in ['ids_once_match','grade_ids_once_match','saved_observations_and_keys_match','totals_match']) for v in it['readers'].values()) for it in checks['iterations']) and checks['final_snapshot_matches_canonical'] and audit['verdict']=='PASS' and not audit['findings'] and checks['final_source_audit']['summary_hash_matches'] and checks['final_two_readers_pass'] and checks['frozen_bank_matches_root'] and not checks['isolated_single_game_catalog_errors'] and gitcheck.returncode==0 and not checks['markdown_trailing_whitespace'] and all(x['exists'] for x in checks['report_local_links'])

seal=load(R/'evidence-seal.json')
checks['original_sealed_artifacts']={'count':len(seal['sha256']),'failures':[rel for rel,h in seal['sha256'].items() if not (R/rel).exists() or sha(R/rel)!=h]}
checks['passed']=checks['passed'] and not checks['original_sealed_artifacts']['failures'] and checks['metadata_authority']['matches_coordinator_capture'] and all(x['corrected_results_valid'] for x in checks['historical_grade_corrections'])
save(R/'stamped-validation.json',checks)
print(json.dumps({k:v for k,v in checks.items() if k not in ['manifest_integrity','original_entry_preservation','iterations','report_local_links']},indent=2))
assert checks['passed'],'See stamped-validation.json for precise failure'
