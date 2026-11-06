"""One-shot version after independent122 challenge and author adjudication."""
from pathlib import Path
import copy, datetime, hashlib, json

R = Path(__file__).resolve().parent
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()
def read(name):
    return json.loads((R/name).read_text())
def write(name, data):
    p = R/name
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('x') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

rev = read('coverage122-independent-closure.json')
q = read('benchmark-v11/questions.json')
k = read('benchmark-v11/answer-key.json')
oldq, oldk = copy.deepcopy(q), copy.deepcopy(k)
q['benchmark_version'] = k['benchmark_version'] = 'benchmark-v12'
decisions = []
for x in rev['proposed_additions']:
    item = copy.deepcopy(x)
    if x['proposed_id'] == 'Q124':
        item['author_decision'] = 'REJECT_MECHANICAL_RECOMBINATION'
        item['author_reason'] = ('The raw Medkit supplies Dress1 Serious OR Heal1 Dressed Serious. '
           'Q16 asks the definitions; Q36 already asks Dress/Heal-dressed branches, Q112 asks Dress1 '
           'and excludes direct undressed Serious healing, Q99 asks others-targeting, Q55 icon legality, '
           'Q61 disposal and Q03 OR/payment. There is no printed undressed-healing exception or new '
           'healing operation. Its subset of existing treatments, changed carrier, dose and cost '
           'do not meet the coordinator novelty criterion. Do not transfer Emergency Room options '
           'to the Item: generic card-text controls remain applicable. Preserve independent proposal '
           'and disagreement; keep complete menu in the summary, without a redundant quiz request.')
    else:
        item['author_decision'] = 'ACCEPT_DISTINCT_PROCEDURE'
        if x['proposed_id'] == 'Q125':
            item['author_reason'] = ('No existing actual stem asks the collective repeated clockwise '
              'two-Action scheduling loop or all-players-passed transition gate. Q04/Q91 cover '
              'individual passing consequences, Q23 draw/token/discards, Q24 Event steps. '
              'This adds actual phase control, not another pass example.')
        else:
            item['author_reason'] = ('Accept only the new coupling/optionality request: one paid Room '
              'Action gives its principal benefit AND may additionally scan, and scan may be declined '
              'without forfeiting that benefit. Q17 asks scan/Surgery scopes, removal, Larva and '
              'Surgery consequences; its volunteered treatment context is not asked. Q45 asks '
              'entry/markers/stack/Fire; Q36/Q112 ask mutually exclusive OR treatments. This '
              'explicit additive-versus-replacement outcome is distinct from merely renaming a '
              'healing carrier or changing its dose. Pair both Rooms in one question.')
        q['questions'].append({'id': x['proposed_id'], 'question': x['proposed_question']})
        k['answers'].append({'id': x['proposed_id'], 'expected_answer': x['proposed_expected_answer'],
                            'source_references': x['raw_source_references'], 'topic': x['topic']})
    decisions.append(item)

key_changes = []
for x in k['answers']:
    if x['id'] in ['Q13','Q32']:
        before = copy.deepcopy(x)
        precision = next(z for z in rev['optional_key_precision'] if z['id'] == x['id'])
        x['expected_answer'] += ' ' + precision['append_or_replace_with']
        x['source_references'] += precision['raw_source_references']
        key_changes.append({'id':x['id'],'before':before,'after':copy.deepcopy(x),
                            'kind':'clarity-only explicit existing requested fact; no new requirement'})
assert q['questions'][:122] == oldq['questions']
assert len(q['questions']) == len(k['answers']) == 124
assert {'Q109','Q124'}.isdisjoint({x['id'] for x in q['questions']})
write('benchmark-v12/questions.json', q)
write('benchmark-v12/answer-key.json', k)
write('benchmark-v12/draft-status.json', {'created_utc':NOW,'candidate':True,'question_count':124,
      'final_readers_dispatched':False,'coverage_closure_pending':True})
with (R/'benchmark-v12/question-bank.md').open('x') as f:
    f.write('# Nemesis — benchmark-v12 candidate\n\n'+q['scope']+'\n\n')
    f.write('\n\n'.join('**'+x['id']+'.** '+x['question'] for x in q['questions'])+'\n')
write('coverage122-author-adjudication.json', {'created_utc':NOW,
      'independent_report':'coverage122-independent-closure.json',
      'independent_report_sha256':sha(R/'coverage122-independent-closure.json'),
      'independent_report_status_preserved':'NON_PASS_ADDITIONS_PROPOSED',
      'novelty_authority':'coverage-novelty-clarification-2026-11-05.json',
      'decisions':decisions,'accepted_ids':['Q125','Q126'],'rejected_id_reserved':'Q124',
      'no_reviewer_PASS_claim':True,'new_candidateN':124,
      'new_final_independent_challenge_required':True,'no_readers_yet':True})
write('benchmark-v12-changes.json', {'created_utc':NOW,'from':'benchmark-v11','to':'benchmark-v12',
      'all_existing122_question_objects_unchanged':True,'original108_questions_unchanged':True,
      'new_ids':['Q125','Q126'],'reserved_ids':['Q109','Q124'],
      'clarity_only_key_changes':key_changes,'source_facts_or_grading_requirements_changed':False,
      'authority':'coverage122-author-adjudication.json'})
rub = read('grading-rubric-v12.json')
rub.update({'rubric_version':'grading-rubric-v13','benchmark_version':'benchmark-v12',
            'fixed_before_final124_readers':NOW,
            'key_clarity_scope':'Q13 Queen Carcass and Q32 noninitiator Trade are already requested general facts. Explicit key expansions do not add unasked subcases, Event routing/discard or an exact phrase requirement.'})
write('grading-rubric-v13.json',rub)
reserved = read('reserved-question-id-history.json')
write('reserved-question-id-history-v2.json',{'prior_history':reserved,
      'reserved_ids':['Q109','Q124'],'Q124':'Rejected independent Medkit proposal, never reader-tested; reserved to preserve proposal identity. Do not reuse for another question.',
      'new_accepted_ids':['Q125','Q126'],'next_unused_id':'Q127'})
print(json.dumps({'candidateN':124,'new_ids':['Q125','Q126'],'reserved_ids':['Q109','Q124'],
                  'summary_unchanged':True,'next_rubric':'grading-rubric-v13.json'}))
