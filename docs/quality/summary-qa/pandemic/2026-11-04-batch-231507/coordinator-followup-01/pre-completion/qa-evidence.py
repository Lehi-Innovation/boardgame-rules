"""Local evidence utilities; never mutates files outside this assigned run."""
import pathlib, json, hashlib, shutil, difflib, sys
ROOT=pathlib.Path(__file__).resolve().parent
REPO=ROOT.parents[4]
PARENT='01a1aa59-9cbf-7673-878d-28aedbe910c3'
def sha(path): return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()
def save(path,obj): pathlib.Path(path).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def freeze(name,benchmark):
    it=ROOT/name;it.mkdir(exist_ok=False)
    shutil.copyfile(REPO/'rules/pandemic.md',it/'summary-snapshot.md')
    shutil.copyfile(ROOT/benchmark/'questions.json',it/'questions.json')
    inputs=[it/'summary-snapshot.md',it/'questions.json',ROOT/benchmark/'answer-key.json',REPO/'extracted/pandemic-rules.txt',ROOT/'matching-publisher-rules.pdf',ROOT/'official-event-puzzle.pdf',ROOT/'forecast-card-photo.jpg',ROOT/'official-components-2.webp']
    save(it/'input-manifest.json',{'benchmark_version':benchmark,'hashes':{str(p):sha(p) for p in inputs},'requested_model':'gpt-6-luna','reasoning_effort':'high'})
    (it/'summary-changes.patch').write_text(''.join(difflib.unified_diff((ROOT/'originals/pandemic.md').read_text().splitlines(True),(it/'summary-snapshot.md').read_text().splitlines(True),fromfile='original/pandemic.md',tofile=name+'/summary-snapshot.md')))
def provenance():
    all_records=[]
    for folder in ['2026/11/04','2026/11/05']:
      for f in pathlib.Path('/mnt/c/Users/jonny/.codex/sessions').joinpath(folder).glob('*.jsonl'):
        with f.open() as fh:
          first=fh.readline()
          try: meta=json.loads(first)
          except json.JSONDecodeError: continue
          payload=meta.get('payload',{}); source=payload.get('source',{})
          if not isinstance(source,dict):continue
          sp=source.get('subagent',{}).get('thread_spawn',{})
          if sp.get('parent_thread_id')!=PARENT:continue
          records=[meta]
          for line in fh:
            if '"type":"turn_context"' in line or '"type": "turn_context"' in line:
              records.append(json.loads(line))
        agent=payload.get('agent_path',sp.get('agent_path'))
        out=ROOT/'runtime-records';out.mkdir(exist_ok=True)
        dest=out/(agent.split('/')[-1]+'.json');save(dest,records)
        contexts=[{'model':x['payload'].get('model'),'effort':x['payload'].get('effort')} for x in records if x['type']=='turn_context']
        all_records.append({'agent_path':agent,'session_id':payload.get('id'),'runtime_file':str(f),'saved_runtime_records':str(dest),'saved_records_sha256':sha(dest),'actual_turn_contexts':contexts,'parent_thread_id':PARENT})
    save(ROOT/'runtime-provenance.json',all_records)
    return all_records
def model_proofs():
    records=provenance();by={x['agent_path'].split('/')[-1]:x for x in records}
    mapping=[('seed-iteration-01','seed_reader'),('seed-iteration-02','seed_retest'),('seed-iteration-03','seed_third'),('seed-iteration-04','seed_fourth'),('expanded-iteration-01','expanded_reader'),('expanded-iteration-02','expanded_second'),('expanded-iteration-03','expanded_third'),('expanded-iteration-04','expanded_fourth'),('expanded-iteration-05','expanded_fifth'),('expanded-iteration-06','expanded_sixth')]
    for name,prefix in mapping:
      if not all(prefix+'_'+r in by for r in ['a','b']):continue
      rs={r:by[prefix+'_'+r] for r in ['a','b']}
      proof={'requested_model':'gpt-6-luna','requested_reasoning_effort':'high','context_isolation':'fork_turns=none; only summary and questions authorized for reading; no stronger filesystem isolation claimed.','runtime_confirmed':all(x['actual_turn_contexts'] and all(c=={'model':'gpt-6-luna','effort':'high'} for c in x['actual_turn_contexts']) for x in rs.values()),'readers':rs}
      if name in ['expanded-iteration-05','expanded-iteration-06']:proof['reader_protocol']='blind-reader-protocol-v2; reader-protocol-revision.json'
      save(ROOT/name/'model-provenance.json',proof)
    reviewers={k:x for k,x in by.items() if k in ['seed_adjudicator','coverage_challenger','independent_source_audit','final_source_auditor','final_source_auditor_v2','final_source_auditor_v3']}
    save(ROOT/'reviewer-model-provenance.json',{'requested_model':'gpt-6.1-sol','requested_reasoning_effort':'high','runtime_confirmed':all(x['actual_turn_contexts'] and all(c=={'model':'gpt-6.1-sol','effort':'high'} for c in x['actual_turn_contexts']) for x in reviewers.values()),'reviewers':reviewers})
def validate():
    checks={}; orig=json.loads((ROOT/'input-manifest.json').read_text())['inputs']
    checks['source_unchanged']=sha(REPO/'extracted/pandemic-rules.txt')==orig['extracted/pandemic-rules.txt']['sha256']
    checks['original_copies_intact']=all(sha(ROOT/'originals'/pathlib.Path(k).name)==v['sha256'] for k,v in orig.items())
    banks={}
    for name in ['benchmark-v1','benchmark-v2','benchmark-v3','benchmark-v4']:
      p=ROOT/name
      qs=json.loads((p/'questions.json').read_text())['questions'];key=json.loads((p/'answer-key.json').read_text())['answers']
      expected=[f'Q{i:02}' for i in range(1,len(qs)+1)]
      checks[name+'_ids']=([q['id'] for q in qs]==[k['id'] for k in key]==expected)
      checks[name+'_frozen_hashes']=all(sha(p/k)==v for k,v in json.loads((p/'frozen-hashes.json').read_text()).items())
      banks[name]=(qs,key)
    for old,new in [('benchmark-v1','benchmark-v2'),('benchmark-v2','benchmark-v3')]:
      checks[old+'_entries_preserved_in_'+new]=all(banks[old][i]==banks[new][i][:len(banks[old][i])] for i in [0,1])
    checks['v3_to_v4_questions_unchanged']=banks['benchmark-v3'][0]==banks['benchmark-v4'][0]
    checks['v3_to_v4_expected_answers_unchanged']=all({k:v for k,v in old.items() if k!='source_references'}=={k:v for k,v in new.items() if k!='source_references'} for old,new in zip(banks['benchmark-v3'][1],banks['benchmark-v4'][1]))
    checks['v3_to_v4_only_Q38_citation_corrected']=all(old==new for old,new in zip(banks['benchmark-v3'][1],banks['benchmark-v4'][1]) if old['id']!='Q38')
    checks['original_20_entries_preserved_in_v4']=all(banks['benchmark-v1'][i]==banks['benchmark-v4'][i][:20] for i in [0,1])
    for it in sorted(ROOT.glob('*iteration-*')):
      if not it.is_dir():continue
      qs=json.loads((it/'questions.json').read_text())['questions'];ids=[q['id'] for q in qs]
      manifest=json.loads((it/'input-manifest.json').read_text());checks[it.name+'_input_integrity']=all(sha(k)==v for k,v in manifest['hashes'].items())
      for r in ['a','b']:
        f=it/f'reader-{r}.json'
        if f.exists():
          a=json.loads(f.read_text())['answers'];checks[it.name+'_reader_'+r+'_ids']=sorted(x['id'] for x in a)==ids
      f=it/'results.json'
      if f.exists():
        results=json.loads(f.read_text())
        benchmark=results['benchmark_version']; expected_key={x['id']:x for x in banks[benchmark][1]}
        checks[it.name+'_questions_match_frozen_benchmark']=qs==banks[benchmark][0]
        for r,rr in results['readers'].items():
          checks[it.name+'_grades_'+r+'_ids']=sorted(x['id'] for x in rr['grades'])==ids
          actual={x['id']:x for x in json.loads((it/f'reader-{r}.json').read_text())['answers']}
          qmap={x['id']:x for x in qs}
          checks[it.name+'_grades_'+r+'_match_inputs']=all(x['question']==qmap[x['id']]['question'] and x['expected_answer']==expected_key[x['id']]['expected_answer'] and x['material_facts']==expected_key[x['id']]['material_facts'] and x['source_references']==expected_key[x['id']]['source_references'] and x['observed_answer']==actual[x['id']]['answer'] and x['reader_evidence']==actual[x['id']]['evidence'] for x in rr['grades'])
          checks[it.name+'_grades_'+r+'_totals']=rr['totals']=={g:sum(x['grade']==g for x in rr['grades']) for g in ['correct','partial','incorrect']}
    save(ROOT/'integrity-validation.json',{'checks':checks,'all_pass':all(checks.values())})
    return checks
def final_validate(name):
    checks=validate();it=ROOT/name
    results=json.loads((it/'results.json').read_text());questions=json.loads((it/'questions.json').read_text())['questions'];n=len(questions)
    checks['final_pair_complete_correct']=all(r['totals']=={'correct':n,'partial':0,'incorrect':0} for r in results['readers'].values())
    checks['final_pair_no_unsupported_guesses']=all(not g['unsupported_guess'] for r in results['readers'].values() for g in r['grades'])
    checks['final_snapshot_matches_canonical']=sha(it/'summary-snapshot.md')==sha(REPO/'rules/pandemic.md')
    audit_path=json.loads((ROOT/'game-status.json').read_text())['source_audit']['path']
    audit=json.loads(pathlib.Path(audit_path).read_text())
    checks['final_source_audit_pass']=audit['verdict']=='PASS' and audit['findings']==[]
    checks['audit_covers_exact_final_bytes']=audit['input_hashes']['summary']['sha256']==sha(it/'summary-snapshot.md')
    checks['audit_sources_intact']=all(sha(x['path'])==x['sha256'] for x in audit['input_hashes']['sources'])
    ledger=json.loads((ROOT/'coverage-ledger.json').read_text());challenge=json.loads((ROOT/'coverage-challenge.json').read_text());resolution=json.loads((ROOT/'coverage-resolution.json').read_text())
    checks['two_consecutive_zero_addition_passes']=all(p['accepted']==[] for p in ledger['passes'][-2:])
    checks['independent_coverage_challenge_resolved']=challenge['new_meaningful_questions']==[] and resolution['all_findings_resolved']
    checks['all_procedural_source_covered']=not json.loads((ROOT/'procedural-coverage-map.json').read_text())['base_core_omitted'] and challenge['coverage_assessment']['saturated_for_assigned_procedural_source']
    proof=json.loads((it/'model-provenance.json').read_text());checks['final_reader_models_effort_confirmed']=proof['runtime_confirmed']
    records=list(proof['readers'].values());final_ids=[x['session_id'] for x in records]
    old_ids=[]
    for old in ROOT.glob('*iteration-*/model-provenance.json'):
      if old.parent!=it:old_ids.extend(x['session_id'] for x in json.loads(old.read_text())['readers'].values())
    checks['final_readers_fresh_distinct_sessions']=len(set(final_ids))==2 and not(set(final_ids)&set(old_ids))
    checks['reviewer_models_effort_confirmed']=json.loads((ROOT/'reviewer-model-provenance.json').read_text())['runtime_confirmed']
    save(ROOT/'final-validation.json',{'final_iteration':name,'benchmark_version':results['benchmark_version'],'question_count':n,'checks':checks,'local_criteria_pass':all(checks.values()),'coordinator_stamping_and_global_checks':'pending; goal remains active'})
    return checks
if __name__=='__main__':
    if sys.argv[1]=='freeze':freeze(sys.argv[2],sys.argv[3])
    elif sys.argv[1]=='provenance':print(json.dumps(provenance(),indent=2))
    elif sys.argv[1]=='validate':print(json.dumps(validate(),indent=2))
    elif sys.argv[1]=='final-validate':print(json.dumps(final_validate(sys.argv[2]),indent=2))
    elif sys.argv[1]=='model-proofs':model_proofs()
