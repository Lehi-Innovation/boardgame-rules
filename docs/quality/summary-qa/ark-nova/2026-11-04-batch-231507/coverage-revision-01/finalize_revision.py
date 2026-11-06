import copy
import hashlib
import json
from pathlib import Path
from build_revision import HERE,QA,DRAFT,BASE,read,write,filehash,oldq,olda,challenge,new,reject,sc01,income

q=read(HERE/'questions.json');a=read(HERE/'answer-key.json');m=read(HERE/'coverage-map.json');ledger=read(HERE/'novelty-rejection-ledger.json')
baseq=read(BASE/'questions.json');basea=read(BASE/'answer-key.json')
assert q['questions'][:20]==baseq['questions']
assert a['answers'][:20]==basea['answers']
assert [r['id'] for r in q['questions']]==[r['id'] for r in a['answers']]
active={r['id'] for r in q['questions']}
assert active=={f'Q{i:02}' for i in range(1,138)}-set(reject)
assert all(set(p['question_ids'])<=active for p in m['passages'])
assert active<={qid for p in m['passages'] for qid in p['question_ids']}
assert next(r for r in a['answers'] if r['id']=='Q17')==sc01['corrected_entry']
assert read(HERE/'SC01-source-key-correction.json')['old_entry']==next(r for r in olda['answers'] if r['id']=='Q17')
for qid in ['Q06','Q42']:
    assert next(r for r in q['questions'] if r['id']==qid)==next(r for r in oldq['questions'] if r['id']==qid)
    assert next(r for r in a['answers'] if r['id']==qid)==next(r for r in olda['answers'] if r['id']==qid)

# Author closure pass3: complete corrected source-map and each challenge finding.
resolutions=[
 {'finding':'F01','decision':'accepted','question_ids':['Q135'],'source_passages':['M02g'],'primary_evidence':'Main pp2/7 Species Diversity tiers5/4/3→5/3/2; Main p13 categories.'},
 {'finding':'F02','decision':'accepted','question_ids':['Q136'],'source_passages':['M18d'],'primary_evidence':'Main pp4–5 complete appeal-income board diagram, applied by Main p18 step5a.'},
 {'finding':'F03','decision':'accepted','question_ids':['Q137'],'source_passages':['M10a','M10d'],'primary_evidence':'Main p10 empty-side up and placement bonus once; Main p6 immediate covered-space bonus.'},
 {'finding':'F04','decision':'accepted_procedure_gap_with_frozen_original_question','question_ids':['Q42','Q133'],'source_passages':['GAB.digging','M13e'],'primary_evidence':'Main p13 Crested Porcupine Digging2 actual options; Glossary p2 dynamic choice timing. Q42 unchanged.'},
 {'finding':'F05','decision':'accepted_explicit_source_key_correction_SC01','question_ids':['Q17'],'source_passages':['M15b'],'primary_evidence':'Main p15 depicted2−/3/4+ bands; Glossary p1 condition as shown; FAQ pp1–2. Corrected benchmark-v1.1 inherited; old key preserved.'},
 {'finding':'F06','decision':'accepted_strict_novelty_rejections','rejected_question_ids':list(reject),'primary_evidence':'Jumping uses Main p7 generic break endpoint; glossary final clarifiers recombine earlier building/support facts; overview genericX abilities reproduce earlier Pouch1/Perception2/Sunbathing2 patterns. All historical entries retained.'},
 {'finding':'F07','decision':'accepted_identity_and_atom_coverage_corrections','question_ids':['Q134','Q133','Q135','Q136','Q137'],'source_passages':['M02c','M02g','M09c','M09f','M10a','M10d','M18d','GAB.digging','M13e'],'primary_evidence':'Main p2 Sea Cave release illustration, Main pp2/7 Species Diversity; Main p9 preserve order/fill deck. Q06 and Q42 unchanged.'},
 {'finding':'F08','decision':'accepted_primary_reference_cleanup','question_ids':['Q131','Q132'],'primary_evidence':'Original English diagrams + official English Icon Overview + narrowly matching original publisher board photograph, cited directly; derived prior report no longer a key authority.'}
]
assert {r['finding'] for r in resolutions}=={f'F{i:02}' for i in range(1,9)}
write('challenge-findings-resolution.json',resolutions)
ledger['closure_passes']=[
 {'pass':3,'target':'After complete revised map: allF01–F08 remedies, explicit original-entry preservation, source/key bands, every new requested fact and novelty reason',
  'addition_count':0,'new_question_ids':[],'findings':'All three accepted source gaps and two missing procedures are explicitly requested. Rejected IDs map only to active earlier questions; all original source passages remain. Every challenge finding has a primary-source resolution. No additional distinct supported rule found.'},
 {'pass':4,'target':'Second full revised-map pass: complete main/glossary/FAQ/Icon Overview index; distinct destinations, counting rules, thresholds, timing, exceptions and diagram payoff cells',
  'addition_count':0,'new_question_ids':[],'findings':'No new distinct supported rule found after the gaps were covered. All63 actually listed Sponsor entries, all supplied ability/map/final clarifiers, FAQ and Icon Overview panels retain coverage. Generic parameter substitutions, ordinary Jumping, and already-tested final-card clarifier combinations do not earn novelty credit. Missing source text is not invented.'}
]
ledger['terminal_zero_addition_passes']=2
ledger['zero_passes_after_complete_revised_map']=True
ledger['next_step']='Parent dispatches a fresh independent source/coverage challenge; these author self-checks do not establish independent final acceptance.'
write('novelty-rejection-ledger.json',ledger)

# Original candidate artifact hashes were sealed before the independent challenge.
sealed=read(DRAFT/'artifact-hashes.json')
immutable={name:{'sealed_sha256':sha,'current_sha256':filehash(DRAFT/name),'unchanged':sha==filehash(DRAFT/name)} for name,sha in sealed.items()}
assert all(v['unchanged'] for v in immutable.values())
write('original-draft-immutability-check.json',immutable)

qmd=['# Ark Nova revised active question bank','','Original English base v1.2 packet plus accepted official English base Icon Overview; original German publisher component artwork supplements obscured numerals only. Solo, Marine Worlds and strategy-guide authority excluded.','',
     '133 active questions retain historical IDs through Q137. Q48, Q109, Q110 and Q126 are rejected duplicate candidates, archived separately; remaining IDs are not renumbered. Original twenty question objects and Q42 are unchanged.','']
amd=['# Ark Nova revised answer key','','Baseline benchmark-v1.1 incorporates explicit SC01 correction to Q17 only. Other nineteen original keys and Q42 are unchanged. Author revision; fresh independent source/coverage acceptance pending.','']
for item,answer in zip(q['questions'],a['answers']):
    qmd += ['**'+item['id']+'** '+item['question'],'']
    amd += ['**'+item['id']+'** '+item['question'],'']
    if item['id']=='Q136':
        amd += ['| Appeal | Money |','|---|---|']+[f'| {span} | {money} |' for span,money in income]+['','Kiosk and activated card/map income are additional.','']
    else:
        amd += [answer['expected_answer'],'']
    amd += ['Source: '+answer['source_references'],'']
(HERE/'question-bank.md').write_text('\n'.join(qmd))
(HERE/'answer-key.md').write_text('\n'.join(amd))

paths=[BASE/'questions.json',BASE/'answer-key.json',QA/'source-key-correction-SC01.json',QA/'coverage-challenge/report.json',
       DRAFT/'questions.json',DRAFT/'answer-key.json',DRAFT/'coverage-map.json',DRAFT/'novelty-rejection-ledger.json',
       QA/'neutral-source-manifest.json',QA/'table-source-check/capstone-icon-overview.pdf',QA/'table-source-check/Spielzene.jpg',QA/'table-source-check/Back_arche_nova.jpg']
repo=QA.parents[4]
paths += [repo/'extracted/ark-nova-rules.txt',repo/'source_pdfs/ark-nova-rules.pdf',repo/'source_pdfs/ark-nova-glossary-rules.pdf',repo/'source_pdfs/ark-nova-faq-rules.pdf']
assert all(p.exists() for p in paths)
write('input-provenance.json',{'role':'author revision after independent source challenge','inputs':[{'path':str(p),'sha256':filehash(p)} for p in paths],
    'not_read':['canonical summary','summary snapshots','reader outputs','grades'],
    'prior_source_reports_are_not_substitutes_for_primary_evidence':True,
    'original_draft_immutable':True,'question_changes_based_on_reader_performance':False})

report='''# Coverage revision 01

This revision has 133 active questions with stable historical IDs through Q137. Q48, Q109, Q110 and Q126 are rejected as duplicate or mechanical-recombination candidates; their original questions, keys, material facts and reasons remain in rejected-candidate-entries.json. Their primary source passages map to earlier real questions. The complete inherited source map is retained and corrected, now 229 passage records.

Five additions cover previously unasked procedures: Q133 Digging2 actual options; Q134 ordered display compaction; Q135 Species Diversity different-category counting and its printed table; Q136 the complete appeal-income table; Q137 newly built standard enclosures empty-side up and once-only placement bonuses. Existing choice/refill timing, sequential funding and numerical examples receive no additional novelty credit.

The first twenty question objects remain unchanged. Their key objects exactly inherit benchmark-v1.1: SC01 explicitly corrects only Q17 to accept depicted printed-standard-size bands2−=1/2,3=3,4+=4/5. The old key17 remains in SC01-source-key-correction.json alongside the correction. Other nineteen original keys are unchanged. Q06 and Q42 question/answer objects remain exactly as in the original candidate; their genuinely missing requested procedures are newQ133/Q134.

All independent findingsF01–F08 have recorded resolutions. Sea Cave/Species Diversity identities and the source map's overbroad coverage claims were corrected. Q131/Q132 now cite primary diagrams and the official English Icon Overview directly, with narrow original publisher component-numeral corroboration, without relying on a prior source report. No canonical summary was read or edited, and no reader output or grade was read. Rejections follow strict source novelty, not reader difficulty or performance.

After all five gaps were covered and the complete revised map regenerated, two further targeted author passes each added zero. This is author self-check evidence only. The original draft's earlier stopping claim was overturned by the independent challenge and remains historical, not independent proof of saturation. A fresh independent source/coverage challenge remains necessary before acceptance.

Canonical authority remains the original English base v1.2 main/glossary/FAQ plus explicitly accepted original official English base Icon Overview. Original publisher German component photographs supply obscured original component numerals only; no German revised prose is adopted. The third-party2022 German card review photo is corroborating research history only. Solo, Marine Worlds, strategy-guide authority, unsupplied card text and absent Map3 clarification remain outside supplied procedural evidence.

Files: questions.json; answer-key.json; material-requested-facts.json; question-bank.md; answer-key.md; coverage-map.json; novelty-rejection-ledger.json; challenge-findings-resolution.json; SC01-source-key-correction.json; rejected-candidate-entries.json; original-draft-immutability-check.json; input-provenance.json; artifact-hashes.json.
'''
(HERE/'coverage-report.md').write_text(report)
hashnames=['questions.json','answer-key.json','material-requested-facts.json','coverage-map.json','novelty-rejection-ledger.json','rejected-candidate-entries.json','SC01-source-key-correction.json','challenge-findings-resolution.json','question-bank.md','answer-key.md','coverage-report.md','original-draft-immutability-check.json','input-provenance.json']
write('artifact-hashes.json',{name:filehash(HERE/name) for name in hashnames})
print('Two post-map zero-addition closure passes recorded. 133 active questions, stable IDs, corrected original20 exact, Q06/Q42 exact; original sealed draft artifacts unchanged.')
