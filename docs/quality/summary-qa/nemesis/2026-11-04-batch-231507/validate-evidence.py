from pathlib import Path
import hashlib,json,collections,subprocess,re
R=Path(__file__).resolve().parent;ROOT=Path('/home/jonny/projects/boardgame-rules');C=ROOT/'rules/nemesis.md';S=ROOT/'extracted/nemesis-rules.txt'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def main():
 initial=read(R/'input-manifest.json');checks={};checks['canonical_source_unchanged']=sha(S)==initial['inputs']['extracted/nemesis-rules.txt']['sha256'];checks['source_snapshot_matches_original']=sha(R/'source-snapshot.txt')==sha(S);checks['original_summary_preserved']=sha(R/'original-summary.md')==initial['inputs']['rules/nemesis.md']['sha256']
 banks={d.name:{'questions':read(d/'questions.json'),'key':read(d/'answer-key.json'),'hashes':{n:sha(d/n) for n in ['questions.json','answer-key.json']}} for d in R.glob('benchmark-*') if d.is_dir() and (d/'questions.json').exists()}
 for name,b in banks.items():
  qi=[x['id'] for x in b['questions']['questions']];ki=[x['id'] for x in b['key']['answers']];checks[name+'_ids_unique_aligned']=qi==ki and len(qi)==len(set(qi))
 for old,new in [('benchmark-v1','benchmark-v2'),('benchmark-v2','benchmark-v3'),('benchmark-v3','benchmark-v4'),('benchmark-v4','benchmark-v5'),('benchmark-v5','benchmark-v6'),('benchmark-v6','benchmark-v7')]:
  x,y=banks[old],banks[new];n=len(x['questions']['questions']);checks[old+'->'+new+'_question_entries_preserved']=x['questions']['questions']==y['questions']['questions'][:n]
  changed=[a['id'] for a,b in zip(x['key']['answers'],y['key']['answers']) if a!=b];checks[old+'->'+new+'_key_changes']=changed
  if old in ['benchmark-v1','benchmark-v2','benchmark-v6']:checks[old+'->'+new+'_key_entries_preserved']=not changed
 iterations={}
 for d in sorted(p for p in R.iterdir() if p.is_dir() and (p/'summary-snapshot.md').exists()):
  manifest=read(d/'input-manifest.json');h=manifest['hashes'];integrity={p:sha(Path(p))==v for p,v in h.items() if Path(p).exists()};info={'input_hashes_match':all(integrity.values()),'input_checks':integrity,'summary_sha256':sha(d/'summary-snapshot.md'),'question_sha256':sha(d/'questions.json'),'matches_canonical':sha(d/'summary-snapshot.md')==sha(C),'cancelled_before_dispatch':(d/'cancelled-before-dispatch.json').exists()}
  if (d/'results.json').exists():
   results=read(d/'results.json');q=read(d/'questions.json')['questions'];expected=[x['id'] for x in q];bank=results['benchmark_version'];key=banks[bank]['key']['answers'];keyby={x['id']:x for x in key};info['readers']={}
   for r in ['a','b']:
    raw=read(d/f'reader-{r}.json')['answers'];grades=results['readers'][r]['grades'];by={x['id']:x for x in raw};gby={x['id']:x for x in grades};ids=[x['id'] for x in raw];gids=[x['id'] for x in grades]
    matches=all(gby[x['id']]['observed_answer']==x['answer'] and gby[x['id']]['expected_answer']==keyby[x['id']]['expected_answer'] for x in raw)
    info['readers'][r]={'count':len(raw),'each_expected_id_once':collections.Counter(ids)==collections.Counter(expected),'each_grade_id_once':collections.Counter(gids)==collections.Counter(expected),'grades_match_raw_and_fixed_key':matches,'counts':results['readers'][r]['counts']}
  iterations[d.name]=info
 prov=read(R/'model-provenance.json') if (R/'model-provenance.json').exists() else {};models=[]
 for x in prov.get('records',[]):
  path=x['agent_path'];turns=x['turn_contexts'];want='gpt-6-luna' if 'reader' in path else 'gpt-6.1-sol';models.append({'agent':path,'runtime_id':x['session_id'],'expected_model':want,'verified':bool(turns) and all(t['model']==want and t['effort']=='high' for t in turns)})
 v={'checks':checks,'banks':{n:{'question_count':len(b['questions']['questions']),'hashes':b['hashes']} for n,b in banks.items()},'iterations':iterations,'actual_models':models,'all_models_confirmed':bool(models) and all(x['verified'] for x in models),'source_gaps':read(R/'source-gaps.json'),'scope':'Validation of artifacts and source fidelity only. Unresolved essential source gaps prevent unconditional QA completion.','canonical_summary_sha256':sha(C),'canonical_source_sha256':sha(S)}
 (R/'validation.json').write_text(json.dumps(v,indent=2)+'\n');print('Validated',len(banks),'banks,',len(iterations),'frozen inputs and',len(models),'agent models')
if __name__=='__main__':main()
