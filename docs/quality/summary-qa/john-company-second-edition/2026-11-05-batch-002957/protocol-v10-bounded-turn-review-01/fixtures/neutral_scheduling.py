"""Review-only ID bookkeeping model. No deployed scheduler, source router or semantic grader."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('neutral_v9', ROOT/'summary-hierarchical-section-check-v9.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)

CONTINUATION = ('Continue this same blind task under the unchanged protocol. Resume the next unfinished '
                'question from your own draft. Complete at most ten additional ordered questions, using '
                'only the original two inputs and your own three files. If all entries and per-ID records '
                'already exist, preserve the first complete draft and finish finalization. A partial turn '
                'is progress only; the entire original bank remains required.')


def status(bank, draft, records, final_exists=False):
    errors = []
    if len(set(bank)) != len(bank): errors.append('invalid bank')
    if len(draft) > len(bank) or draft != bank[:len(draft)]: errors.append('not exact original ordered prefix')
    if len(records) != len(set(records)) or set(records) != set(draft): errors.append('per-ID source records do not cover completed prefix exactly')
    complete = not errors and draft == bank and set(records) == set(bank)
    if final_exists and not complete: errors.append('premature final file')
    return {'valid_bookkeeping': not errors, 'full_bank_complete': complete and not errors,
            'next_id': bank[len(draft)] if not errors and len(draft)<len(bank) else None,
            'completed_prefix_count':len(draft), 'errors':errors}


def turn(before, after, initial_receipt_complete=True):
    errors=[]
    if not initial_receipt_complete and after: errors.append('write before full initial receipt')
    if after[:len(before)] != before: errors.append('prior completed prefix changed')
    if not 0 <= len(after)-len(before) <= 10: errors.append('turn delta outside 0..10')
    return {'valid_bookkeeping':not errors,'additional_completed':len(after)-len(before),'errors':errors}


RESULTS=[]


def test(name, category, fn, predicate):
    try: observed=fn()
    except Exception as e: observed={'exception':type(e).__name__,'message':str(e)}
    RESULTS.append({'name':name,'category':category,'observed':observed,'matches':bool(predicate(observed))})


BANK=[f'N{i:03}' for i in range(1,24)]
valid=lambda x:x['valid_bookkeeping']
invalid=lambda x:not x['valid_bookkeeping']
test('zero_prefix_progress_not_complete','prefix',lambda:status(BANK,[],[]),lambda x:valid(x) and not x['full_bank_complete'] and x['next_id']=='N001')
test('ten_prefix_progress_not_complete','prefix',lambda:status(BANK,BANK[:10],BANK[:10]),lambda x:valid(x) and not x['full_bank_complete'] and x['next_id']=='N011')
test('twenty_prefix_progress_not_complete','prefix',lambda:status(BANK,BANK[:20],BANK[:20]),lambda x:valid(x) and not x['full_bank_complete'] and x['next_id']=='N021')
test('full_prefix_is_complete','prefix',lambda:status(BANK,BANK,BANK,True),lambda x:valid(x) and x['full_bank_complete'] and x['next_id'] is None)
test('premature_final_rejected','prefix',lambda:status(BANK,BANK[:10],BANK[:10],True),invalid)
test('source_record_serialization_order_irrelevant','prefix',lambda:status(BANK,BANK[:10],list(reversed(BANK[:10]))),valid)
test('full_answer_bank_missing_last_source_record_not_final','prefix',lambda:status(BANK,BANK,BANK[:-1],True),invalid)
test('duplicate_source_record_rejected','prefix',lambda:status(BANK,BANK[:2],[BANK[0],BANK[0],BANK[1]]),invalid)
test('missing_source_record_rejected','prefix',lambda:status(BANK,BANK[:10],BANK[:9]),invalid)
test('source_record_ahead_rejected_until_reconciled','prefix',lambda:status(BANK,BANK[:9],BANK[:10]),invalid)
test('out_of_order_prefix_rejected','prefix',lambda:status(BANK,[BANK[1],BANK[0]],[BANK[1],BANK[0]]),invalid)
test('skipped_id_rejected','prefix',lambda:status(BANK,[BANK[0],BANK[2]],[BANK[0],BANK[2]]),invalid)
test('duplicate_id_rejected','prefix',lambda:status(BANK,[BANK[0],BANK[0]],[BANK[0],BANK[0]]),invalid)
test('invented_id_rejected','prefix',lambda:status(BANK,['N999'],['N999']),invalid)
test('eleven_additional_rejected','turn',lambda:turn([],BANK[:11]),invalid)
test('ten_additional_allowed','turn',lambda:turn([],BANK[:10]),valid)
test('later_ten_additional_allowed','turn',lambda:turn(BANK[:10],BANK[:20]),valid)
test('last_three_additional_allowed','turn',lambda:turn(BANK[:20],BANK),valid)
test('early_stop_three_allowed','turn',lambda:turn([],BANK[:3]),valid)
test('zero_progress_is_no_completion_guarantee','turn',lambda:turn([],[]),lambda x:valid(x) and x['additional_completed']==0)
test('initial_write_before_full_receipt_rejected','delivery',lambda:turn([],BANK[:1],False),invalid)
test('prefix_regression_rejected','turn',lambda:turn(BANK[:10],BANK[:9]),invalid)
test('prior_prefix_replacement_rejected','turn',lambda:turn(BANK[:2],[BANK[1],BANK[0],BANK[2]]),invalid)


def schedule(n, chunks):
    bank=BANK[:n];done=[];events=[];initial_full_bytes=None
    for count in chunks:
        before=done[:];done=bank[:min(n,len(done)+count)]
        t=turn(before,done)
        s=status(bank,done,done)
        assert t['valid_bookkeeping'] and s['valid_bookkeeping']
        if s['full_bank_complete'] and initial_full_bytes is None:
            initial_full_bytes=json.dumps({'completed_ids':done},ensure_ascii=False,indent=2).encode()+b'\n'
        events.append({'delta':t['additional_completed'],'count':len(done),'complete':s['full_bank_complete'],'next':s['next_id']})
    assert events[-1]['complete'] and initial_full_bytes is not None
    return {'events':events,'first_full_sha256':hashlib.sha256(initial_full_bytes).hexdigest()}


for n,chunks in [(1,[1]),(10,[10]),(11,[10,1]),(20,[10,10]),(23,[10,10,3]),(23,[3,10,10])]:
    test(f'schedule_{n}_'+ '_'.join(map(str,chunks)),'schedule',lambda n=n,chunks=chunks:schedule(n,chunks),lambda x:'events' in x and x['events'][-1]['complete'])


def freeze_bytes():
    first=json.dumps({'completed_ids':BANK},indent=2).encode()+b'\n'
    draft=first
    final=json.loads(draft)
    final['revision_notes']=['Neutral bookkeeping metadata repair.']
    final_bytes=json.dumps(final,ensure_ascii=False).encode()
    assert draft==first and hashlib.sha256(draft).hexdigest()==hashlib.sha256(first).hexdigest()
    assert final_bytes != draft
    reserialized=json.dumps(json.loads(draft),separators=(',',':')).encode()
    assert json.loads(reserialized)==json.loads(draft) and reserialized != draft
    return {'unchanged_draft_hash':hashlib.sha256(draft).hexdigest(),
            'final_differs':True,'semantically_identical_reserialization_would_violate_byte_preservation':True}


test('first_full_draft_frozen_final_repair_separate','preservation',freeze_bytes,lambda x:x.get('final_differs') is True)


def same_actor(identity_before,identity_after,message):
    return {'same_actor':identity_before==identity_after,'continuation_is_constant_template':message==CONTINUATION}


test('same_actor_constant_continuation','blindness-bookkeeping',lambda:same_actor('opaque-reader-A','opaque-reader-A',CONTINUATION),lambda x:all(x.values()))
test('fresh_replacement_is_not_continuation','blindness-bookkeeping',lambda:same_actor('opaque-reader-A','opaque-reader-B',CONTINUATION),lambda x:not x['same_actor'])


def prefix_checker():
    # These strings are newly authored neutral fixtures, not external question/answer files.
    text='## Labels\nKeep labels dry.\n';u=checker.units(text)['T001']
    questions=[{'id':i,'question':'What should be kept dry?'} for i in BANK]
    answers=[]
    for i in BANK[:10]:
        answers.append({'id':i,'clause_ledger':[{'requested_clause':'What should be kept dry','section_ids':['T001'],'fact_kind':'lookup'}],
                        'case_conclusions':[],'operative_sections':[{k:v for k,v in u.items() if k!='text'}],
                        'answer':'Applicable summary text\n'+checker.attachment(u),'support':'supported','evidence':[]})
    partial=checker.check_data(text,questions,{'answers':answers},'neutral')
    reduced=checker.check_data(text,questions[:10],{'answers':answers},'neutral')
    return {'full_original_bank':{k:partial[k] for k in ['question_count','answer_count','exact_ordered_unique_ids','all_structure_and_declared_source_spans_valid']},
            'incorrectly_reduced_bank':{k:reduced[k] for k in ['question_count','answer_count','exact_ordered_unique_ids','all_structure_and_declared_source_spans_valid']}}


test('unchanged_checker_requires_original_bank_for_completeness','checker-limitation',prefix_checker,
     lambda x:x['full_original_bank']['all_structure_and_declared_source_spans_valid'] is True
     and x['full_original_bank']['exact_ordered_unique_ids'] is False
     and x['incorrectly_reduced_bank']['exact_ordered_unique_ids'] is True)


if __name__=='__main__':
    result={'purpose':'Review-only scheduling/schema bookkeeping, not adopted enforcement or factual QA.',
            'python_version':sys.version,'synthetic_bank_ids':BANK,'generic_continuation_template':CONTINUATION,
            'count':len(RESULTS),'matches':sum(x['matches'] for x in RESULTS),'cases':RESULTS}
    (ROOT/'neutral-results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'count':result['count'],'matches':result['matches']}))
    for x in RESULTS:
        if not x['matches']:print(json.dumps(x))
    raise SystemExit(0 if result['count']==result['matches'] else 1)
