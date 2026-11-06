import hashlib
import json
import re
from pathlib import Path
from build_expansion import rows, PASS1_END, PASS2_END, PASS3_END, PASS4_END, PASS5_END, PASS6_END

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
q=json.loads((HERE/'questions.json').read_text())
a=json.loads((HERE/'answer-key.json').read_text())
m=json.loads((HERE/'coverage-map.json').read_text())
seedq=json.loads((HERE.parent/'benchmark-v1/questions.json').read_text())
seeda=json.loads((HERE.parent/'benchmark-v1/answer-key.json').read_text())
assert q['questions'][:20]==seedq['questions']
assert a['answers'][:20]==seeda['answers']
assert [x['id'] for x in q['questions']]==[x['id'] for x in a['answers']]
assert [x['id'] for x in q['questions']]==[f'Q{i:02}' for i in range(1,len(q['questions'])+1)]
mapped={qid for p in m['passages'] for qid in p['question_ids']}
assert all(r['id'] in mapped for r in rows)
sp={p['passage_id'] for p in m['passages'] if p['passage_id'].startswith('GSP.')}
assert all('GSP.'+str(i) in sp for i in range(201,265))

qmd=['# Ark Nova expanded question bank', '', q['scope']+' Supplemented by the accepted official base Icon Overview and original component numeric evidence.', '', 'Original Q01–Q20 are unchanged. Q21 onward add distinct source-backed rules.', '']
amd=['# Ark Nova expanded answer key','','Author-written source-backed expectations; independent coverage challenge remains pending.','']
facts={}
for item,answer in zip(q['questions'],a['answers']):
    qmd += ['**'+item['id']+'** '+item['question'],'']
    fact_list=answer.get('material_requested_facts')
    if fact_list is None:
        fact_list=[x.strip() for x in answer['expected_answer'].split(';') if x.strip()]
    facts[item['id']]={'material_requested_facts':fact_list,'source_references':answer['source_references'],'origin':'seed-verbatim-with-clause-index' if int(item['id'][1:])<=20 else 'authored-source-expansion'}
    amd += ['**'+item['id']+'** '+item['question'],'',answer['expected_answer'],'','Source: '+answer['source_references'],'']
(HERE/'question-bank.md').write_text('\n'.join(qmd))
(HERE/'answer-key.md').write_text('\n'.join(amd))
(HERE/'material-requested-facts.json').write_text(json.dumps(facts,indent=2,ensure_ascii=False)+'\n')

ends=[PASS1_END,PASS2_END,PASS3_END,PASS4_END,PASS5_END,PASS6_END]
names=[
 'Main rules, golden rules and complete glossary animal ability pass',
 'Every listed individual Sponsor clarification, grouping genuinely identical patterns',
 'Final scoring, advanced maps, FAQ restrictions and component diagram pass',
 'Newly accepted full official base Icon Overview and printed card effect pass',
 'Reputation track numerical and glyph source gap closure',
 'Map A all seven support bonuses and timing glyph cross-check']
passes=[]
start=0
for i,(end,name) in enumerate(zip(ends,names),1):
    passes.append({'pass':i,'target':name,'new_question_ids':[r['id'] for r in rows[start:end]],'addition_count':end-start,'source_map_complete_after_pass':i==6})
    start=end
passes += [
 {'pass':7,'target':'Post-map targeted audit: all glossary ability names, Sponsor entries201–264, final clarifiers, map entries, FAQ and Icon Overview panels; question/key requested-fact alignment',
  'addition_count':0,'new_question_ids':[], 'findings':'All 63 actually listed individual Sponsor entries map to questions; 223 has no supplied entry. No unmapped authored question. Question wording expanded where necessary to ask already-keyed facts; no new rule branch. Duplicate card examples map to generalized effects.'},
 {'pass':8,'target':'Second post-map targeted audit: consequential timing, target eligibility, effect destinations, capacities, thresholds, losses/retentions, exceptions and diagram glyphs across all four rules documents',
  'addition_count':0,'new_question_ids':[], 'findings':'No additional supported rule/outcome branch found. Confirmed seven Map A outputs, reputation ranges/bonuses, donation ladder, Hypnosis slot limit, Pilfering two targets, terrain adjacency, support token destinations, final scoring and upgrade timing. Source boundary remains explicit; no invented absent card or Map3 text.'}]
rejected=[
 {'candidate':'Separate per-player-count copies of setup/break/project-cap questions','decision':'reject_cosmetic_recombination','covered_by':['Q02','Q05','Q16'],'reason':'All distinct player-count branches are already explicitly requested; merely substitute player count.'},
 {'candidate':'Separate numerical Cards draw-table question for every strength','decision':'group_shared_table','covered_by':['Q25','Q26'],'reason':'Complete source tables cover every distinct draw/discard threshold without five numerical variants.'},
 {'candidate':'Separate same-effect Sponsors for each of Sponsorship231–235 and any-zoo specialists236–240','decision':'group_shared_pattern','covered_by':['Q88','Q89'],'reason':'Questions explicitly require each category mapping and shared reward; effect destination, scope and all income thresholds retained.'},
 {'candidate':'Repeated fallback enclosure questions for release, relocation and each sample animal','decision':'reuse_existing_distinct_branches','covered_by':['Q13','Q17'],'reason':'Both procedures and all three consequential fallback branches are already requested, including no legal size.'},
 {'candidate':'FAQ move all animals as a new question','decision':'reuse_existing','covered_by':['Q13'],'reason':'Original Q13 already requests which and how many may move; existing key explicitly includes all eligible animals with individual choices.'},
 {'candidate':'FAQ refill display after every income player as a new question','decision':'reuse_existing','covered_by':['Q19'],'reason':'Original question and key already request this exact timing branch.'},
 {'candidate':'FAQ partner discount doubles as a separate new question','decision':'reuse_existing','covered_by':['Q11','Q30'],'reason':'OriginalQ11 includes double continent reduction; new general icon rules add the separate exclusion of left conditions.'},
 {'candidate':'More rep-over15 numerical examples','decision':'reject_cosmetic_variant','covered_by':['Q07'],'reason':'One appeal per remaining step is already explicit.'},
 {'candidate':'Full Map3 printed special ability or omitted Sponsor223 text','decision':'reject_missing_source_passage','covered_by':[],'reason':'Neither has an additional supplied procedural passage. Do not infer from external summaries, another edition or strategy-guide prose. General chosen-map special-ability rule remains covered.'},
 {'candidate':'Unseen Animal-card abilities or every numerical version of Hunter/Perception/Scavenging','decision':'reject_unsupported_or_cosmetic','covered_by':['Q45','Q57','Q95','Q98','Q126','Q130'],'reason':'Packet glossary, overview and actually illustrated effects are covered. Entire unsupplied Animal-card deck is not invented.'},
 {'candidate':'Solo setup/rounds/challenge and solo break exception','decision':'exclude_scope','covered_by':[],'reason':'Explicitly excluded. Multiplayer option to replace interactive effects with printed alternate effects is a base multiplayer rule and is retained in Q39.'},
 {'candidate':'Background colors, decorative component quantities, recommended hands and photographic credits as separate questions','decision':'exclude_nonprocedural_or_presentation','covered_by':['Q10','Q18','Q19','Q20'],'reason':'Effect timing is assessed; visual encoding, inventory and recommendations do not add a rule/outcome branch.'},
 {'candidate':'Marine Worlds, German revised rules or strategy-guide procedural claims','decision':'exclude_scope_and_authority','covered_by':[],'reason':'No such authority was used. Supplemental original German product photography supplies matching component numerals only; original English base prose governs.'}]
accepted=[{'id':r['id'],'coverage_section':r['coverage_section'],'decision':'add_distinct_material_rule_or_exception','new_requested_facts':r['material_requested_facts'],'source_references':r['source_references']} for r in rows]
ledger={'game':'Ark Nova','original_count':20,'expanded_count':len(q['questions']),'addition_count':len(rows),'original20_exact':True,'source_map_complete':True,'open_source_gaps':[],
 'passes':passes,'terminal_consecutive_zero_addition_passes':2,'zero_passes_occur_after_complete_source_map':True,
 'accepted_candidates':accepted,'rejected_or_grouped_candidates':rejected,'independent_final_audit_claimed':False,'next_step':'Parent dispatches a fresh independent coverage challenger; author closure is not independent coverage acceptance.'}
(HERE/'novelty-rejection-ledger.json').write_text(json.dumps(ledger,indent=2,ensure_ascii=False)+'\n')

manifest={}
for file in ['questions.json','answer-key.json','coverage-map.json','material-requested-facts.json','novelty-rejection-ledger.json','question-bank.md','answer-key.md']:
    manifest[file]=hashlib.sha256((HERE/file).read_bytes()).hexdigest()
(HERE/'artifact-hashes.json').write_text(json.dumps(manifest,indent=2)+'\n')
report=f'''# Authored coverage expansion

Prepared {len(q['questions'])} questions: original twenty preserved exactly, plus {len(rows)} source-backed additions. The complete source map contains {len(m['passages'])} passage records, with {sum(p['disposition']=='covered' for p in m['passages'])} covered and {sum(p['disposition']=='excluded' for p in m['passages'])} explicit exclusions/boundaries. Every new question is mapped. All actually listed individual Sponsor clarifications are mapped, as are every supplied glossary ability, final-scoring clarification, advanced-map clarification, FAQ entry and official Icon Overview panel.

Six sequential authoring/source passes were followed by two consecutive zero-addition targeted passes after the source map was complete. See novelty-rejection-ledger.json for additions, grouped patterns, rejected variants and checks. These are author self-checks. A fresh independent coverage challenger remains the next step; no independent final audit or final source saturation acceptance is claimed here.

Canonical scope remains the original English BASE v1.2 main rules, base glossary and official base FAQ. The parent explicitly accepted the original official English Icon Overview as an additional primary base rules aid. It adds interaction target selection and several icon procedures omitted from prose. The original publisher photographs of matching original German component artwork close hidden numeric table cells: Animals II1/1/2/2/2. A coordinator-supplied third-party 2022 review photograph of an original German card is retained only as corroborating research history, not user firsthand or English-card evidence. Original publisher photography also clarifies tiny reputation numerals, with their glyph meanings decoded from the official English Icon Overview. This is a narrow original-component supplement; it adopts no German revised rules, Marine Worlds content or strategy-guide authority. Canonical source files and summary were not edited.

The complete combined extracted source was read, all three supplied PDFs were extracted with project .venv PyMuPDF and inspected, and the newly accepted two-page official Icon Overview was read and visually inspected. Source-only reports under ../table-source-check document the supplementary provenance. No canonical summary, summary snapshot, reader answer or grade was read by this author.

Absent Map3 clarification and Sponsor223 glossary entry are source boundaries, not exclusions of printed rules. General use of the chosen map ability is covered. Unsupplied individual card text is not invented. Solo-specific rules and Marine Worlds are outside scope; the base multiplayer option to use alternate interactive effects is included because the supplied main rules and FAQ explicitly authorize it.

Outputs: questions.json, answer-key.json, question-bank.md, answer-key.md, material-requested-facts.json, coverage-map.json, novelty-rejection-ledger.json. Original twenty keys remain byte-for-byte equivalent as parsed objects; their material fact clause index is kept separately to preserve those objects exactly.
'''
(HERE/'coverage-report.md').write_text(report)
print('Validated expanded question/key IDs, exact original twenty, all new questions mapped and all listed Sponsors indexed.')
print(f'{len(q["questions"])} questions; closure passes 7 and 8 each add zero; independent challenge pending.')
