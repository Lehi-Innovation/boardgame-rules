"""Run-local QA integrity helpers. Only this game's evidence is written."""
from pathlib import Path
import argparse,collections,difflib,hashlib,json,shutil
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[4]
CANON=REPO/'rules/john-company-second-edition.md'
SOURCE=REPO/'extracted/john-company-second-edition-rules.txt'
PARENT_ID='01a1aaa2-7c89-7c92-bca8-a89efc3fe4d7'
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def save(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def provenance():
    records=[]
    for f in Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/05').glob('*.jsonl'):
        meta=None; contexts=[]
        try:
            with f.open() as fh:
                for line in fh:
                    d=json.loads(line)
                    if d.get('type')=='session_meta':
                        meta=d['payload'];source=meta.get('source',{})
                        spawn=source.get('subagent',{}).get('thread_spawn',{}) if isinstance(source,dict) else {}
                        if spawn.get('parent_thread_id')!=PARENT_ID:break
                    elif d.get('type')=='turn_context':
                        c=d['payload'];settings={k:c[k] for k in ['model','effort'] if k in c}
                        if settings not in contexts:contexts.append(settings)
                        break
            source=(meta or {}).get('source',{})
            spawn=source.get('subagent',{}).get('thread_spawn',{}) if isinstance(source,dict) else {}
            if spawn.get('parent_thread_id')==PARENT_ID:
                records.append({'agent':spawn['agent_path'],'session_id':meta['id'],'runtime_source':str(f),'parent_thread_id':PARENT_ID,'settings':contexts,'confirmed':bool(contexts)})
        except (ValueError,OSError):continue
    return records
def freeze(benchmark,iteration,previous=None):
    b=ROOT/benchmark;p=b/iteration;p.mkdir(exist_ok=False)
    shutil.copyfile(CANON,p/'summary-snapshot.md');shutil.copyfile(b/'questions.json',p/'questions.json')
    save(p/'input-manifest.json',{'benchmark_version':benchmark,'requested_model':'gpt-6-luna','requested_effort':'high','parent_thread_id':PARENT_ID,'inputs':{str(x):digest(x) for x in [CANON,SOURCE,b/'answer-key.json',p/'summary-snapshot.md',p/'questions.json']}})
    if previous:
        old=Path(previous);old=old if old.is_absolute() else ROOT/old
        patch=''.join(difflib.unified_diff(old.read_text().splitlines(keepends=True),CANON.read_text().splitlines(keepends=True),fromfile=str(old),tofile=str(CANON)))
        (p/'summary-changes.patch').write_text(patch)
    return p
def validate_iteration(benchmark,iteration):
    b=ROOT/benchmark;p=b/iteration;qs=read(b/'questions.json')['questions'];ks=read(b/'answer-key.json')['answers'];ids=[q['id'] for q in qs]
    checks={'question_ids_unique':len(ids)==len(set(ids)),'key_ids_match':[k['id'] for k in ks]==ids,'question_copy_identical':(p/'questions.json').read_bytes()==(b/'questions.json').read_bytes(),'canonical_snapshot_identical':CANON.read_bytes()==(p/'summary-snapshot.md').read_bytes(),'readers':{}}
    for role in ['a','b']:
        o=p/f'reader-{role}.json'
        if o.exists():
            a=read(o)['answers'];got=[x['id'] for x in a]
            checks['readers'][role]={'count':len(a),'exact_ids':collections.Counter(got)==collections.Counter(ids),'no_duplicates':len(got)==len(set(got)),'evidence_present':all(x.get('evidence') for x in a)}
    manifest=read(p/'input-manifest.json');checks['frozen_hashes_intact']={path:digest(path)==expected for path,expected in manifest.get('inputs',manifest.get('hashes',{})).items() if path!=str(CANON)}
    records=provenance();save(p/'model-provenance.json',{'requested_model':'gpt-6-luna','requested_effort':'high','records':records,'isolation':'Fresh fork_turns none; readers only frozen summary+questions. Instruction isolation, shared filesystem.'})
    save(p/'validation.json',checks);return checks
def enrich(benchmark,iteration):
    b=ROOT/benchmark;p=b/iteration
    if (p/'results.json').exists():raise FileExistsError('Preserve existing grades')
    a=read(p/'independent-adjudication.json');qs={x['id']:x for x in read(b/'questions.json')['questions']};ks={x['id']:x for x in read(b/'answer-key.json')['answers']}
    out={'benchmark_version':benchmark,'independent_adjudication':'independent-adjudication.json','grading_policy':'Every requested material fact per answer; equivalent wording accepted, no borrowing facts, omissions distinct from contradictions; source-backed unsupported guesses cannot pass.','readers':{}}
    for role in ['a','b']:
        raw={x['id']:x for x in read(p/f'reader-{role}.json')['answers']};rv=a['readers'][f'reader-{role}'];grades=[]
        for g in rv.get('answers',rv.get('grades',rv.get('adjudications',[]))):
            z=dict(g);i=g['id'];z['grade']=g['grade'].capitalize();z.update(question=qs[i]['question'],expected_answer=ks[i]['expected_answer'],source_references=ks[i]['source_references'],observed_answer=raw[i]['answer'],reader_support_label=raw[i].get('support'),summary_evidence=raw[i].get('evidence'));grades.append(z)
        if collections.Counter(z['id'] for z in grades)!=collections.Counter(qs.keys()):raise ValueError('Missing or duplicate grade IDs; preserve raw grader report and fix adapter')
        out['readers'][f'reader-{role}']={'grades':grades,'counts':{x:sum(z['grade']==x for z in grades) for x in ['Correct','Partial','Incorrect']}}
    out['status']='PASS' if all(x['counts']['Correct']==len(qs) and x['counts']['Partial']==x['counts']['Incorrect']==0 and all(not z.get('unsupported_guesses') and not z.get('unsupported_correct_guesses') for z in x['grades']) for x in out['readers'].values()) else 'FAILED'
    save(p/'results.json',out);return {k:v['counts'] for k,v in out['readers'].items()}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('command',choices=['freeze','validate','provenance','enrich']);ap.add_argument('benchmark',nargs='?');ap.add_argument('iteration',nargs='?');ap.add_argument('--previous');a=ap.parse_args()
    if a.command=='freeze':print(freeze(a.benchmark,a.iteration,a.previous))
    elif a.command=='validate':print(json.dumps(validate_iteration(a.benchmark,a.iteration),indent=2))
    elif a.command=='enrich':print(json.dumps(enrich(a.benchmark,a.iteration),indent=2))
    else:save(ROOT/'model-provenance.json',{'records':provenance()})
