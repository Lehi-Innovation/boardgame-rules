from pathlib import Path
import hashlib
import json

R=Path(__file__).parent
B=R/'expanded-candidate-07'
D=B/'review-inputs'
assert not D.exists()
D.mkdir()
def read(p): return json.loads(p.read_text())
def save(p,d): p.write_text(json.dumps(d,separators=(',',':'),ensure_ascii=False)+'\n')
scope=read(B/'question-scope-map-candidate.json')
items=[]
for e in scope['questions']:
    if 'facts' not in e:
        items.append({'id':e['id'],'status':e['status'],'instruction':'Map the complete current literal question/key afresh.'})
        continue
    overrides=[]
    for f in e['facts']:
        if f['classification']!='asked' or f['required_material']!=f['raw_key_fact'] or f.get('documentary_conditional'):
            overrides.append({key:f[key] for key in ['fact_id','key_index','classification','required_material','unasked_context','documentary_conditional','reachable_core_novelty_credit']})
    items.append({'id':e['id'],'raw_fact_count':len(e['facts']),'clauses':e['clauses'],'scope_overrides':overrides,'equivalents':e['equivalents']})
save(D/'proposed-asked-scope.json',{'status':'Carry-forward proposal; needs NEW independent validation against current literal question/key.','bank_version':B.name,'default_fact_scope':'For unchanged entries, each unlisted raw key fact is asked as written and identified by question-Fnn with zero-based key index. Scope overrides below replace that default; they are complete required/context distinctions, not hints to readers. Every raw fact must be accounted for in new reviewer output.','source_policy':'Key citations are locators; primary text/images control. Only actual asked material earns coverage credit.','questions':items,'withdrawn':scope['withdrawn'],'equivalence_policy':scope['equivalence_policy']})
coverage=read(B/'coverage-map.json')
for e in coverage['original_fifty_printed_abilities']:
    e.pop('tested_claims',None)
# Compact repetitive locator metadata without removing any source unit/disposition.
for e in coverage['applicable_2018_faq']:
    e.pop('seed_explicitly_asked_by',None)
    e.pop('candidate_ids',None)
save(D/'coverage-map.json',coverage)
passes=read(B/'targeted-coverage-passes.json')
passes['passes'] += [
 {'pass':11,'focus':'After independent02 additions: original setup and complete phase sequence, who chooses targets, launch/alliance placement, original draw triggers/non-triggers, reward entitlement/mandatory collection, reinforcement operation and all ordinary destinations.','qualifying_rule_additions':0,'new_questions':[],'rejections':['Further ordinary attack/reward quantities repeat the already asked rule, not a distinct branch.','The new complete seven-phase sequence adds the missing overall order; Start Turn remains separately tested and earns no second novelty credit.','Offense and offensive-ally placement are explicit inQ158; defensive placement remainsQ007.','Negative ordinary draw events now explicitly asked inQ157; replacement windows remainQ016.'],'authority_recheck':'Primary passages for all seven additions reread; parent reviewed current questions/key additions and all original core source-unit mappings. No additional rule found.'},
 {'pass':12,'focus':'After independent02 additions: current versus printed card identity for resolution, actual asked scope of all original50 powers and general flare/card rules, accepted FAQ rows versus exclusions and documentary conditionals.','qualifying_rule_additions':0,'new_questions':[],'rejections':['Another modified-Morph number is not a new identity rule.','Listing another example of a covered resolution category does not establish a new branch absent changed timing/priority/exception.','Unasked generic reminders or named examples do not become scoring requirements.','No primary original-base copying/sheet-stealing/duplicate-Morph/all-foreign-planets enabler was newly established.'],'authority_recheck':'Complete current source/key scope overlay and all non-asked/mixed records checked; prior complete source/native image inspections remain authority. No further qualifying rule found.'}
]
passes['status']='Two renewed parent targeted zero-addition passes for presently source-resolvable scope; fresh independent03 source/scope challenge and actual human choices still pending.'
save(D/'targeted-coverage-passes.json',passes)
(B/'targeted-coverage-passes-after-review.json').write_text(json.dumps(passes,indent=2,ensure_ascii=False)+'\n')
save(D/'input-manifest.json',{'question_count':160,'raw_key_fact_records':519,'sha256':{str(p.relative_to(B)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [B/'questions.json',B/'answer-key.json',B/'acceptance-rejection-ledger.json',B/'versioned-corrections.json',B/'withdrawn-question-ledger.json',*D.iterdir()] if p.is_file()}})
print([(p.name,p.stat().st_size) for p in D.iterdir()])
