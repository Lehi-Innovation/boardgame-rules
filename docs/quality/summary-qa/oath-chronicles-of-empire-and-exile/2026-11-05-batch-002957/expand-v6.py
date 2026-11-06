from pathlib import Path
import copy, datetime, hashlib, json, shutil
P = Path(__file__).resolve().parent
V = P/'expanded-v6'
V.mkdir(exist_ok=False)
def J(path): return json.loads(path.read_text())
def H(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def W(path, data): path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
proposal = J(P/'coverage-review-06.json')['accepted_new_questions'][0]
q = J(P/'expanded-v5/questions.json'); k = J(P/'expanded-v5/answer-key.json')
q['benchmark_version'] = k['benchmark_version'] = 'expanded-v6'
q['questions'].append({'id':'Q101','question':proposal['question']})
key = {'id':'Q101','expected_answer':proposal['expected_answer'],
       'material_facts':proposal['new_material_facts'],
       'source_references':'Law printed p3 setup box before step19; Law1.19–20; Law8.8'}
k['answers'].append(key)
assert q['questions'][:100] == J(P/'expanded-v5/questions.json')['questions']
assert k['answers'][:100] == J(P/'expanded-v5/answer-key.json')['answers']
W(V/'questions.json',q); W(V/'answer-key.json',k)
text = ['# Oath expanded benchmark v6', '', '101 retained regression questions. Ten historical overlaps retain zero novelty credit. The count follows uncapped source challenges. All100 prior question and key entries remain exactly unchanged; Q101 adds only the deferred-rebuild setup prerequisite.', '']
for a,b in zip(q['questions'], k['answers']):
    text += ['## '+a['id'],'',a['question'],'','**Answer:** '+b['expected_answer'],'','**Source:** '+b['source_references'],'']
(V/'question-bank.md').write_text('\n'.join(text))
scope = J(P/'expanded-v5/grading-scope.json')
scope['benchmark_version'] = 'expanded-v6'
scope['created_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
scope['reader_answers_inspected_for_this_scope'] = True
scope['new_Q101_answers_inspected'] = False
scope['preparation_disclosure'] = 'All100 prior scope entries (319 facts) copied exactly without amendment. Historical v5 reader responses have been inspected, but no Q101 response exists; its one requested trigger/order fact and contextual exclusions are frozen before fresh v6 dispatch.'
scope['inputs']['questions'] = 'expanded-v6/questions.json'
scope['inputs']['fixed_key'] = 'expanded-v6/answer-key.json'
scope['questions'].append({'id':'Q101','question':proposal['question'],
 'fixed_key_expected_answer_sha256':hashlib.sha256(key['expected_answer'].encode()).hexdigest(),
 'source_references':key['source_references'],
 'asked_clause_map':[{'clause_id':'Q101-C01','asked_clause':'May setup draws precede the deferred rebuild? At what point must rebuilding occur?', 'required_fact_ids':['Q101-F01'], 'rationale':'One explicit setup prerequisite governs both asked clauses.'}],
 'required_facts':[{'fact_id':'Q101-F01','expected_fact':'If the previous Chronicle did not rebuild the world deck, rebuild before regional discard seeding and before starting-adviser bottom draws; do not perform those draws from the unrebuilt stack and rebuild afterward.', 'basis':'Law p3 gold setup box, before step19; source-grounded reviewer06 discovery'}],
 'contextual_exclusions':[{'key_or_source_fact':'Repeated10+2/15+3/rest rebuild recipe and exact numbered Law step labels', 'classification':'contextual_not_independently_required','rationale':'The question asks trigger and order, already established recipe has zero novelty credit. A clear operational before-any-seeding/dealing answer suffices without Law step numbers.','contradiction_policy':'Absence not penalized; materially false volunteered recipe/order still incorrect.'}],
 'contextual_exclusion_status':'Only the deferred-trigger/setup-prerequisite fact is independently required.',
 'semantic_notes':'Before seeding regional discards and dealing starting advisers is the operational equivalent of before Law step19. Do not demand the summary\'s step numbers match the original Law numbering.'})
assert scope['questions'][:100] == J(P/'expanded-v5/grading-scope.json')['questions']
W(V/'grading-scope.json', scope)
inputs = [V/'questions.json',V/'answer-key.json',P/'expanded-v5/grading-scope.json',P/'coverage-review-06.json',Path('/home/jonny/projects/boardgame-rules/extracted/oath-current-law.txt')]
W(V/'grading-scope-manifest.json',{'artifact_type':'grading-scope SHA256 freeze manifest','benchmark_version':'expanded-v6','created_utc':scope['created_utc'], 'scope_artifact':{'path':str((V/'grading-scope.json').resolve()),'sha256':H(V/'grading-scope.json')},'input_files':[{'path':str(x.resolve()),'sha256':H(x)} for x in inputs], 'required_fact_count':320,'question_count':101,'all_prior_scope_entries_exactly_preserved':True,'frozen_before_reader_dispatch':True})
shutil.copyfile(P/'coverage-ledger.json',P/'coverage-ledger-before-v6.json')
ledger = J(P/'coverage-ledger.json')
ledger['accepted_questions'].append({'id':'Q101','source_references':[key['source_references']], 'novelty':proposal['new_material_facts'][0], 'accepted':True,'reviewer_proposal':'coverage-review-06 A01; identified before parent summary disclosure; final saturation requires fresh reviewer'})
ledger['coverage_map']['Law p3 deferred world-deck rebuild prerequisite before setup19']=['Q101']
ledger['passes'].append({'pass':17,'focus':'Adjudicate fresh complete-delivery reviewer06 challenge','count':1,'accepted_ids':['Q101'],'novelty_credit':1,'repeated_recipe_credit':0})
ledger['passes'].append({'pass':18,'focus':'Reopen Law1–8/full Playbook setup, actions, Campaign, victory, Chronicle handoff after deferred-rebuild addition','count':0,'accepted_ids':[], 'rejections':[{'candidate':'Repeat setup rebuild recipe or adviser bottom-draw example','reason':'Q020/Q024 retain existing facts, Q101 now tests previously missing deferred trigger and prerequisite.'},{'candidate':'Illustrated Forest Temple card-specific Chronicle preservation power','reason':'Generic printed-card priority is already tested; arbitrary individual card recall is outside core procedural expansion, as distinguished by reviewer06. No source rule is removed.'}]})
ledger['passes'].append({'pass':19,'focus':'Reopen all Site/Card Reference, Law9–10, full errata and procedural source map; no numerical or actor-name recombinations credited','count':0,'accepted_ids':[], 'rejections':[{'candidate':'More glossary, site or endgame quantitative permutations','reason':'Existing explicit generic branches and conditions determine these without a new source-defined rule.'},{'candidate':'Deferred rebuild described as a new Chronicle recipe','reason':'Recipe is existing Q020; the only new prerequisite is already Q101, so this receives zero further novelty credit.'}]})
ledger['stopping_rule']={'consecutive_zero_addition_passes':2,'passes':[18,19],'all_core_procedural_passages_mapped':True,'independent_challenge':{'verdict':'PENDING','report':'coverage-review-07.json','reason':'Reviewer06 disclosed summary content after its independent gap discovery; it is historical discovery, not final independence gate.'}}
W(P/'coverage-ledger.json',ledger)
shutil.copyfile(P/'coverage-ledger.json',P/'coverage-ledger-reviewed-07.json')
W(V/'freeze-manifest.json',{'question_count':101,'novelty_credited_questions':91,'retained_historical_overlaps':10,'hashes':{x.name:H(x) for x in [V/'questions.json',V/'answer-key.json',V/'grading-scope.json']},'prior100_questions_and_keys_unchanged':True,'summary_unchanged':True})
print('Frozen expanded-v6:101questions,320requiredfacts; rootpasses18/19 zero; fresh reviewer required.')
