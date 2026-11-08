"""Correct a pre-blind question's unsupported destination demand, preserving history."""
from pathlib import Path
import copy
import hashlib
import json

R=Path(__file__).parent
OLD=R/'expanded-candidate-07'
OUT=R/'expanded-candidate-08'
assert not OUT.exists()
OUT.mkdir()
def read(p): return json.loads(p.read_text())
def save(name,obj): (OUT/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
q,k=read(OLD/'questions.json'),read(OLD/'answer-key.json')
q['benchmark_version']=k['benchmark_version']=OUT.name
index=next(i for i,e in enumerate(q['questions']) if e['id']=='Q146')
before=copy.deepcopy(q['questions'][index])
q['questions'][index]['question']='Using the classic Filch Wild flare, what items may you illicitly take and from which locations, where may the retrieved ships go, when must the flare be revealed and when may it be zapped, what happens if caught, and what changes about the deck/discards after it is revealed?'
save('questions.json',q);save('answer-key.json',k)
assert q['questions'][:20]==read(R/'seed-v1/questions.json')['questions']
assert k['answers'][:20]==read(R/'seed-v1/answer-key.json')['answers']
assert q['questions'][:index]+q['questions'][index+1:]==read(OLD/'questions.json')['questions'][:index]+read(OLD/'questions.json')['questions'][index+1:]
assert k['answers']==read(OLD/'answer-key.json')['answers']
correction={'parent_version':OLD.name,'question_id':'Q146','kind':'genuine-source-scope-question-precision-correction-before-any-expanded-blind-test','before_question':before,'after_question':q['questions'][index],'unchanged_key':k['answers'][index],'primary_source':'Original rulebook p5 classic Filch Wild illustration, extraction lines399–413','operative_source_boundary':'The text explicitly supplies warp ships to colonies and card sources deck/discard; it does not explicitly supply an illicit-card destination. No destination is invented.','independent_scope_finding':'SCOPE04-031, actual-question-scope-validation-04.json','independent_primary_source_adjudication':'Continuing reviewer02 own original rulebook/FAQ/native-source review, message and forthcoming alien-cross-source-continuation-02.json; no explicit illicit-card destination found.','rule_removed_from_source_coverage':False,'new_qualifying_rule':False,'reason':'The original broad to-where phrase could demand a detail absent from supplied primary effect text. Current wording asks both item sources and the expressly printed ship destination. All other sourced classic Filch mechanics and every raw key fact remain.','expanded_reader_answers_seen':False,'original_twenty_preserved_verbatim':True}
save('versioned-corrections.json',correction)
ledger=read(OLD/'acceptance-rejection-ledger.json')
ledger.append({'candidate':'SCOPE04-031/primary-source precision','question_id':'Q146','decision':'correct-unsupported-question-demand-in-new-version','primary_source':correction['primary_source'],'reason':correction['reason'],'new_qualifying_rule':False})
save('acceptance-rejection-ledger.json',ledger)
for name in ['candidate-question-map.json','withdrawn-question-ledger.json','targeted-coverage-passes-after-review.json']:
    save(name,read(OLD/name))
scope=read(R/'source-review/actual-question-scope-map-04.json')
scope.update(bank_version=OUT.name,status='Carry-forward independently validated07 scope; only source-exact Q146 wording requires continuing-validator confirmation.')
entry=next(e for e in scope['questions'] if e['id']=='Q146')
entry['updated_literal_question']=q['questions'][index]['question']
entry['scope_validation']='Prior mapping preserved; new source-exact literal wording awaits validator04 own continuation. No card destination invented.'
save('question-scope-map-candidate.json',scope)
coverage=read(OLD/'coverage-map.json')
coverage.update(bank_version=OUT.name,question_count=160,status='Question precision08 applied without a new rule; composite source/overlap review and Planning source-scope adjudication pending.')
coverage['question_precision_correction']=correction
coverage['pending_source_scope_candidate']='FAQp8 Planning commitment case: primary-source applicability adjudicator06 running; no original-only outcome adopted.'
save('coverage-map.json',coverage)
(OUT/'question-bank.md').write_text('# Expanded candidate 08 — composite review pending\n\n'+'\n\n'.join(f"## {qe['id']}\n\n{qe['question']}\n\n"+'\n'.join('- '+f for f in ke['required_facts']) for qe,ke in zip(q['questions'],k['answers']))+'\n')
save('input-manifest.json',{'review_candidate_only':True,'question_count':160,'raw_key_fact_records':519,'original_twenty_preserved_verbatim':True,'all_raw_key_entries_identical_to07':True,'only_literal_question_changed':'Q146','sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.is_file()}})
print(OUT.name,len(q['questions']),sum(len(a['required_facts']) for a in k['answers']))
