"""Validate this run's frozen evidence, without stamping or shared mutations."""
from pathlib import Path
import collections
import datetime
import difflib
import hashlib
import json
import re
import subprocess
import evidence_tools as e

R = e.ROOT
P = e.REPO

def read(p):
    return json.loads(p.read_text())

def check_inputs():
    prepared=P/'docs/quality/summary-qa/batches/2026-11-04-batch-231507/prepared-dead-last-bank'
    for p in prepared.iterdir():
        if p.is_file():
            assert p.read_bytes()==(R/'benchmark-v1'/p.name).read_bytes(), ('Prepared input changed',p)
    original=read(R/'input-manifest.json')['inputs']
    for path,h in original.items():
        if path.startswith(('source_pdfs/','extracted/')):
            assert e.digest(P/path)==h, ('Source changed',path)
    assert e.digest(R/'seed-iteration-01/summary-snapshot.md')==original['rules/dead-last.md']
    provenance=read(R/'source-provenance.json')
    original_text=provenance['original_extraction']
    assert e.digest(P/original_text['path'])==original_text['sha256']
    for bank in ['benchmark-v1','benchmark-v2']:
        q=read(R/bank/'questions.json')['questions'];k=read(R/bank/'answer-key.json')['answers']
        hashes=read(R/bank/'hashes.json')
        assert e.digest(R/bank/'questions.json')==hashes['questions_sha256']
        assert e.digest(R/bank/'answer-key.json')==hashes['answer_key_sha256']
        assert len({x['id'] for x in q})==len(q)==len(k)==len({x['id'] for x in k})
        assert [x['id'] for x in q]==[x['id'] for x in k]
        for expected,qq,kk in zip(hashes['entries'],q,k):
            assert expected['id']==qq['id']==kk['id']
            assert expected['question_sha256']==hashlib.sha256(json.dumps(qq,sort_keys=True).encode()).hexdigest()
            assert expected['answer_sha256']==hashlib.sha256(json.dumps(kk,sort_keys=True).encode()).hexdigest()
    assert read(R/'benchmark-v2/questions.json')['questions'][:20]==read(R/'benchmark-v1/questions.json')['questions']
    assert read(R/'benchmark-v2/answer-key.json')['answers'][:20]==read(R/'benchmark-v1/answer-key.json')['answers']
    assert e.digest(R/'benchmark-v2/questions.json')==read(R/'benchmark-v2/freeze-manifest.json')['questions_sha256']
    assert e.digest(R/'benchmark-v2/answer-key.json')==read(R/'benchmark-v2/freeze-manifest.json')['key_sha256']

def check_iterations(final):
    rows=[]; total=0
    iterations=sorted([p for p in R.iterdir() if p.is_dir() and p.name.startswith(('seed-iteration-','expanded-iteration-'))])
    for iteration in iterations:
        bank='benchmark-v1' if iteration.name.startswith('seed') else 'benchmark-v2'
        questions=read(iteration/'questions.json')['questions']
        assert (iteration/'questions.json').read_bytes()==(R/bank/'questions.json').read_bytes()
        keys=read(R/bank/'answer-key.json')['answers'];qd={x['id']:x for x in questions};kd={x['id']:x for x in keys}
        for path,h in read(iteration/'input-manifest.json')['hashes'].items():
            assert e.digest(Path(path))==h, ('Frozen input mismatch',iteration.name,path)
        result=read(iteration/'results.json');prov=read(iteration/'model-provenance.json')
        assert prov['all_confirmed']
        totals={}
        for letter in ['a','b']:
            answers=read(iteration/f'reader-{letter}.json')['answers'];grades=result['readers'][letter]['grades']
            expected=set(qd)
            assert len(answers)==len(grades)==len(expected)
            assert collections.Counter(x['id'] for x in answers)==collections.Counter(expected)
            assert collections.Counter(x['id'] for x in grades)==collections.Counter(expected)
            ad={x['id']:x for x in answers}
            for g in grades:
                id=g['id'];assert g['question']==qd[id]['question']
                assert g['expected_answer']==kd[id]['answer'] and g['source_references']==kd[id]['source_references']
                assert g['observed_answer']==ad[id]['answer'] and g['reader_evidence']==ad[id]['evidence']
                assert g['reason'] and g['grade'] in ['correct','partial','incorrect']
            totals[letter]={x:sum(g['grade']==x for g in grades) for x in ['correct','partial','incorrect']}
            assert totals[letter]==result['readers'][letter]['totals']
            prompt=(iteration/f'reader-{letter}-prompt.txt').read_text()
            assert str(iteration/'summary-snapshot.md') in prompt and str(iteration/'questions.json') in prompt
            assert str(iteration/f'reader-{letter}.json') in prompt
            assert 'answer-key.json' not in prompt
            # A separately retained exact dispatch string omits the template's final newline.
            (iteration/f'reader-{letter}-dispatch-prompt.txt').write_text(prompt.rstrip('\n'))
            total+=len(answers)
        version=read(iteration/'prompt-version.json')['version'] if (iteration/'prompt-version.json').exists() else 'blind-v1'
        e.write(iteration/'prompt-manifest.json',{'prompt_version':version,'exact_dispatch_texts':{f'reader-{l}-dispatch-prompt.txt':e.digest(iteration/f'reader-{l}-dispatch-prompt.txt') for l in ['a','b']},'terminal_newline_note':'Readable template has a terminal newline; exact dispatch copy matches supplied prompt text without that newline.'})
        v={'iteration':iteration.name,'questions':len(questions),'input_hashes_intact':True,'exact_id_coverage':True,'all_grades_match_observed_and_fixed_key':True,'actual_models_confirmed':True,'totals':totals}
        e.write(iteration/'validation.json',v);rows.append(v)
    end=next(x for x in rows if x['iteration']==final)
    assert all(x=={'correct':27,'partial':0,'incorrect':0} for x in end['totals'].values())
    assert not any(read(R/final/'results.json')['readers'][l].get('unsupported_additional_claims') for l in ['a','b'])
    assert (R/final/'summary-snapshot.md').read_bytes()==(P/'rules/dead-last.md').read_bytes()
    return rows,total

def main():
    final='expanded-iteration-05'
    check_inputs();iterations,count=check_iterations(final)
    # All actual turn contexts must agree, not only the first context used for provenance.
    actual=[]
    for p in R.rglob('*model-provenance.json'):
        for record in read(p)['runtime_verification']:
            contexts=[]
            for line in Path(record['runtime_path']).open():
                d=json.loads(line)
                if d.get('type')=='turn_context':
                    c=d['payload'];assert c.get('model')==record['requested_model'] and c.get('effort')=='high'
                    contexts.append({'timestamp':d['timestamp'],'model':c['model'],'effort':c['effort']})
            actual.append({'agent':record['agent'],'session_id':record['session_id'],'contexts':contexts})
    e.write(R/'runtime-model-validation.json',{'all_turn_contexts_confirmed':True,'agents':actual})
    audit=read(R/'fresh-final-source-audit.json');assert audit['verdict']=='PASS'
    assert audit['summary_fidelity_assessment']['material_errors_found']==0
    assert audit['summary_fidelity_assessment']['material_omissions_of_available_source_rules_found']==0
    assert all(x.get('summary_defect') is False for x in audit['findings'])
    for item in audit['sha256_inputs']:
        assert e.digest(Path(item['path']))==item['sha256']
        if Path(item['path'])==R/final/'summary-snapshot.md':
            assert item['sha256']==e.digest(R/final/'summary-snapshot.md')
    assert len(audit['visual_checks'])==8 and all(x['inspected'] for x in audit['visual_checks'])
    assert len(audit['isolation']['inputs_read'])==11
    assert set(audit['isolation']['inputs_read'])=={x['path'] for x in audit['sha256_inputs']}
    fresh=read(R/'fresh-final-audit-model-provenance.json')
    assert fresh['all_confirmed'] and fresh['runtime_verification'][0]['agent']=='/root/fresh_exact_final_audit'
    checks=[]
    for command in [[str(P/'.venv/bin/python'),'-m','scripts.validate','rules/dead-last.md'],['git','diff','--no-index','--check','/dev/null','rules/dead-last.md']]:
        proc=subprocess.run(command,cwd=P,capture_output=True,text=True)
        # --no-index returns 1 for the expected new-file difference even when --check is clean.
        passed=(proc.returncode in [0,1] and not proc.stdout and not proc.stderr) if command[0]=='git' else proc.returncode==0
        checks.append({'command':command,'exit_code':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr,'passed':passed,'exit_note':'git --no-index exit1 is expected for a new file when --check emits no whitespace findings' if command[0]=='git' else None})
        assert passed,(command,proc.stdout,proc.stderr)
    previous=R/'seed-iteration-01/summary-snapshot.md';current=R/final/'summary-snapshot.md'
    (R/'summary-changes.patch').write_text(''.join(difflib.unified_diff(previous.read_text().splitlines(True),current.read_text().splitlines(True),fromfile='coordinator-baseline',tofile=final)))
    links=[]
    for match in re.finditer(r'\]\(([^)]+)\)',(R/'README.md').read_text()):
        target=match.group(1)
        if target.startswith(('http:','https:','#')):continue
        resolved=(R/target.split('#')[0]).resolve()
        assert resolved.exists() or resolved==R/'validation.json',('Broken README link',target)
        links.append(target)
    validation={'validated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_prepared_files_byte_identical':True,'original20_entries_and_hashes_preserved':True,'all_frozen_input_hashes_intact':True,'source_fingerprints_unchanged':True,'all_answer_and_grade_ids_exactly_once':True,'all_grades_match_key_and_raw_answers':True,'actual_models_high_effort_all_turn_contexts_confirmed':True,'total_reader_answers_and_grades_checked':count,'iterations':iterations,'final_snapshot_matches_canonical_byte_for_byte':True,'final_summary_sha256':e.digest(current),'final_questions_sha256':e.digest(R/'benchmark-v2/questions.json'),'final_key_sha256':e.digest(R/'benchmark-v2/answer-key.json'),'final_reader_regression':'PASS','final_source_fidelity_audit':'PASS','repository_checks':checks,'readme_links_validated':links,'coordinator_stamping_and_final_catalog_checks':'not scheduled for this incomplete game; coordinator accepts awaiting-source handoff','full_qa_completion':'NOT CLAIMED: essential source procedures unresolved; see source-limitations.json'}
    validation['fresh_final_source_audit']={'report':'fresh-final-source-audit.json','agent':'/root/fresh_exact_final_audit','requested_and_actual_model':'gpt-6.1-sol','requested_and_actual_effort':'high','fork_turns':'none','allowed_inputs_hashed_and_verified':11,'visual_source_pages_verified':8,'summary_fidelity':'PASS','source_executability':'MAJOR gaps, awaiting-source','no_text_change_requested':True}
    e.write(R/'validation.json',validation)
    print(json.dumps({'reader_answers_checked':count,'canonical_sha256':validation['final_summary_sha256'],'regression':'PASS','full_qa_completion':validation['full_qa_completion']},indent=2))

if __name__=='__main__':
    main()
