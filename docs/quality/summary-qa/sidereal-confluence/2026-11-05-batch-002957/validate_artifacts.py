from pathlib import Path
import json,hashlib,sys,collections
ROOT=Path(__file__).resolve().parent
CANONICAL=Path('/home/jonny/projects/boardgame-rules/rules/sidereal-confluence.md')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def check_banks():
 report=[]
 for d in sorted(ROOT.iterdir()):
  if not d.is_dir() or not (d/'freeze.json').exists():continue
  freeze=json.loads((d/'freeze.json').read_text())
  integrity={n:sha(d/n)==h for n,h in freeze['hashes'].items()};assert all(integrity.values()),(d,integrity)
  q=json.loads((d/'questions.json').read_text())['questions'];k=json.loads((d/'answer-key.json').read_text())['answers'];f=json.loads((d/'asked-facts.json').read_text())['questions'];ids=[x['id'] for x in q]
  assert ids==[x['id'] for x in k]==[x['id'] for x in f] and len(ids)==len(set(ids))
  assert all(a['required_facts']==b['required_facts'] and a['contextual_background']==b['contextual_background'] and c['question']==b['question'] for a,b,c in zip(k,f,q))
  facts=[v['id'] for a in k for v in a['required_facts']];assert len(facts)==len(set(facts))
  report.append({'bank':d.name,'question_count':len(ids),'required_fact_count':len(facts),'frozen_hashes_intact':integrity,'unique_question_ids':True,'unique_fact_ids':True,'scope_map_equals_key':True})
 return report
if __name__=='__main__':
 banks=check_banks();m=json.loads((ROOT/'source-manifest.json').read_text());sourcechecks=[{'path':x['path'],'sha256':x['sha256'],'intact':sha(x['path'])==x['sha256']} for x in m['sources']];assert all(x['intact'] for x in sourcechecks)
 oldq=json.loads((ROOT/'seed-v1/questions.json').read_text())['questions'];oldk=json.loads((ROOT/'seed-v1/answer-key.json').read_text())['answers']
 preservation=[]
 for d in sorted(ROOT.iterdir()):
  if not d.is_dir() or not (d/'freeze.json').exists():continue
  q=json.loads((d/'questions.json').read_text())['questions'];k=json.loads((d/'answer-key.json').read_text())['answers'];sameq=q[:20]==oldq
  changed=[a['id'] for a,b in zip(k[:20],oldk) if a['expected_answer']!=b['expected_answer']]
  assert sameq and set(changed)<={'Q08'}
  preservation.append({'bank':d.name,'original20_IDs_and_wording_unchanged':sameq,'expected_answer_changes_from_seed_v1':changed,'correction_note':'Q08 pre-reader seed-v2 source/scope correction explicitly versioned; other original expected answers unchanged. Required-atom scope corrections are versioned separately; all original versions retain original hashes.'})
 out={'status':'PASS for checks performed','bank_integrity':banks,'original_entry_preservation':preservation,'source_checks':sourcechecks,'canonical_sha256':sha(CANONICAL),'final_gates_not_implied':'Bank/source integrity does not assert final blind-reader/audit/coverage PASS.'}
 dest=ROOT/(sys.argv[1] if len(sys.argv)>1 else 'integrity-check.json');assert not dest.exists(),'Refuse historical output overwrite';dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print('Integrity PASS:',len(banks),'frozen bank versions,',len(sourcechecks),'sources; originals preserved')
