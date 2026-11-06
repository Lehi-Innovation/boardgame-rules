import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent;QA=HERE.parent;PRIOR=QA/'coverage-revision-01'
def read(path):return json.loads(path.read_text())
def write(name,value):(HERE/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
q=read(HERE/'questions.json');a=read(HERE/'answer-key.json');facts=read(HERE/'material-requested-facts.json');m=read(HERE/'coverage-map.json');ledger=read(HERE/'novelty-rejection-ledger.json')
oldq=read(PRIOR/'questions.json');olda=read(PRIOR/'answer-key.json')
reject={'Q65','Q84','Q101','Q128'}
active={r['id'] for r in q['questions']}
assert len(active)==131
assert active=={r['id'] for r in oldq['questions']}-reject|{'Q138','Q139'}
assert [r['id'] for r in q['questions']]==[r['id'] for r in a['answers']]
assert active==set(facts)
for old,now in [(oldq['questions'],q['questions']),(olda['answers'],a['answers'])]:
    for r in old:
        if r['id'] not in reject:assert r==next(x for x in now if x['id']==r['id'])
assert q['questions'][:20]==oldq['questions'][:20]
assert a['answers'][:20]==olda['answers'][:20]
assert all(set(p['question_ids'])<=active for p in m['passages'])
assert active<={qid for p in m['passages'] for qid in p['question_ids']}
assert len({p['passage_id'] for p in m['passages']})==231
assert all(set(r['procedure_covered_by'])<=active for r in m['shared_source_lookup_facts'])

# Both author closure passes follow the addition pass and the completed revised map.
ledger['closure_passes']=[
 {'pass':2,'target':'Full33-page source-to-question pass after both gaps covered and revised map complete; embedded-card outcomes and disposal destinations',
  'addition_count':0,'new_ids':[],
  'findings':'Immediate all-zoos capped Lynx aggregation now explicitlyQ138; FinalScoring return-under-own-pile nowQ139. Other embedded cards instantiate existing Hunter, Perception, Scavenging, Sprint, Multiplier, Boost, Digging, Venom, Flock, Pack or unique-building procedures. All former source passages retained; lookup-only values distinguished from new procedures. No further distinct supported rule found.'},
 {'pass':3,'target':'Second targeted source-to-question pass: counting scope, effect destinations, timing, limits, exceptions, every glossary/FAQ/Icon panel and map diagram',
  'addition_count':0,'new_ids':[],
  'findings':'No additional distinct supported rule found. All63 listed Sponsor clarifications remain mapped, with ordinary numeric lookup values retained without extra novelty credit. No active coverage edge points to any archived question. Complete-table cells stay grouped; absent component text, odd rounding and solo/expansion rules are not invented.'}
]
ledger['terminal_zero_addition_passes']=2
ledger['zero_passes_after_both_current_gaps_and_complete_map']=True
ledger['next_step']='Parent obtains a fresh independent saturation challenge; author self-checks do not establish independent acceptance.'
write('novelty-rejection-ledger.json',ledger)

inventory=read(HERE/'primary-reading-inventory.json')
reading={'role':'author primary-source reading for revision02, not an independent audit','total_pdf_pages_read':33,
 'all_primary_pdf_pages_native_text_and_full_page_visuals_read':True,
 'native_text_bounded_read_ranges':{
   'main-complete-primary-text.txt':[[1,300],[301,600],[601,900],[901,1179],['tail',2]],
   'glossary-complete-primary-text.txt':[[1,270],[271,544],['tail',4]],
   'faq-complete-primary-text.txt':'Complete file printed and read',
   'icons-complete-primary-text.txt':'Complete file printed and read after whitespace-only normalization to suppress enormous native diagram spacing; no words removed'},
 'truncated_ranges':[],'end_lines_without_newline_recovered':True,
 'pdf_inventory':inventory,
 'full_page_visual_sheets':['main-pages-1-4.jpg','main-pages-5-8.jpg','main-pages-9-12.jpg','main-pages-13-16.jpg','main-pages-17-20.jpg','glossary-pages-1-4.jpg','glossary-pages-5-8.jpg','faq-pages-1-3.jpg','icons-pages-1-2.jpg'],
 'embedded_card_text_targeted_reading':[
  {'primary_pages':'Main2/7','procedure':'CheetahSprint3, ScienceLab, SeaCave release, SpeciesDiversity, LargeAnimalZoo and Action tables','coverage':'Q25–Q27,Q61,Q17,Q129,Q130,Q135; exact illustrated card names/tables are not inferred from omitted deck text.'},
  {'primary_pages':'Main4–9','procedure':'Board payout/rep/map cells and CaracalHunter2, WhiteStorkBuildMultiplier, LionPack2, LeopardHunter4 illustrations','coverage':'Q131,Q132,Q136 and existing Hunter/Multiplier/own-icon rules. Changed counts/names do not add questions. Own enlarged display-printed-cards.png inspected.'},
  {'primary_pages':'Main11–12','procedure':'VultureScavenging3, CaimanSnapping1, OwlPerception4, MarabouScavenging2, Veterinarian and LynxIconicAnimalEurope','coverage':'Q130,Q58,Q95,Q63 existing patterns; Q138 adds the previously missing immediate capped all-zoos aggregate. Own lynx-effect-full.png and owl-marabou-veterinarian-full.png recover complete printed lines.'},
  {'primary_pages':'Main13','procedure':'AnacondaConstriction/Clever, CrestedPorcupineDigging2, BadgerBoostAnimals and CobraVenom2','coverage':'Q38–Q42,Q59,Q125,Q133,Q134 cover existing procedures; own digging-venom-printed-cards.png inspected. No extra parameter-only questions.'},
  {'primary_pages':'Main14–19','procedure':'Association/donation diagrams, Release bands and Sunbathing example, MeerkatDen, final-card illustrations and FinalScoring discard text','coverage':'Existing Q17,Q29,Q92,Q111,Q112,Q129; newQ139 requested precise p18 deck destination. Own final-scoring-discard-full.png inspected.'}
 ],
 'solo_page20_and_solo_FAQ_inspected_but_excluded':True,
 'canonical_summary_reader_outputs_grades_and_repair_history_read':False,
 'prior_question_key_objects_not_rewritten':True}
for item in inventory:
    textpath=HERE/item['complete_text_file']
    item['native_line_count_including_unterminated_last_line']=len(textpath.read_text().splitlines())
write('source-reading-report.json',reading)

qmd=['# Ark Nova active question bank — revision02','','131 active questions retain historical IDs throughQ139. Newly archived duplicate candidatesQ65/Q84/Q101/Q128 are recorded separately. All other question wording and key objects remain unchanged from revision01, including the corrected original twenty.','']
amd=['# Ark Nova answer key — revision02','','All retained key objects are unchanged. Q138/Q139 add the two primary-source gaps. Author revision; independent saturation acceptance remains pending.','']
for question,answer in zip(q['questions'],a['answers']):
    qmd += ['**'+question['id']+'** '+question['question'],'']
    amd += ['**'+question['id']+'** '+question['question'],'',answer['expected_answer'],'','Source: '+answer['source_references'],'']
(HERE/'question-bank.md').write_text('\n'.join(qmd))
(HERE/'answer-key.md').write_text('\n'.join(amd))

assert all(item['unchanged'] for group in read(HERE/'prior-artifact-immutability-check.json').values() for item in group.values())
checks={'active_question_count':131,'highest_historical_id':'Q139','retained_question_and_answer_objects_exact':True,'corrected_original20_exact':True,'Q06_Q42_exact':True,
    'new_ids':['Q138','Q139'],'archived_ids':sorted(reject,key=lambda x:int(x[1:])),
    'no_active_dead_coverage_edges':True,'source_passage_records':231,'all_original_passage_ids_retained':True,
    'two_author_zero_addition_passes_after_complete_revised_map':True,'prior_draft_and_revision01_sealed_artifacts_unchanged':True,'independent_acceptance_claimed':False}
write('validation-report.json',checks)

inputs=[PRIOR/name for name in ['questions.json','answer-key.json','material-requested-facts.json','coverage-map.json','novelty-rejection-ledger.json']]+[QA/'coverage-challenge-02/report.json']
inputs += [Path(item['file']) for item in inventory]
write('input-provenance.json',{'inputs':[{'path':str(p.resolve()),'sha256':digest(p)} for p in inputs],
  'only_written_directory':str(HERE),'prior_derived_reports_not_used_as_primary_authority':True,'forbidden_summary_readers_grades_history_not_read':True})
report='''# Coverage revision02

131 active questions retain historical IDs throughQ139. NewQ138 tests the Eurasian Lynx printed immediate aggregate:1appeal per Europe icon across all players zoos, capped at8. NewQ139 tests returning a discarded FinalScoring card facedown underneath the remaining FinalScoringpile. Exact primary locations are MainPDFp12 embedded Lynx cards and MainPDFp18 10conservation bullet.

Q65,Q84,Q101,Q128 are archived as standalone numeric/named lookup combinations. Complete old entries and independent reasons are retained. Their printed amounts, terrain associations and university diagram cell remain in shared-source-lookup-facts.json, while the procedures map to earlier active real questions. Q84 does not depend on archivedQ65. All other question/key objects, including corrected benchmark-v1.1 original twenty and Q06/Q42, remain exactly unchanged. Earlier rejected IDs are not reused or renumbered.

The complete inherited source map has231 records, including all previous passage IDs plus explicit Lynx and FinalScoring-discard records. M12b/M18b overclaims are corrected. All C02-F01–F03 findings have recorded resolutions. All63 actually listed Sponsor entries, glossary abilities/maps/final clarifiers, FAQ entries and IconOverview panels remain indexed. Parameter-only cards and one-cell table variants do not receive novelty credit.

All33 authorized PDF pages were reread in bounded complete native-text ranges and full-page visual sheets. Embedded cards were enlarged, including the Lynx twice-printed effect, Owl/Marabou/Veterinarian, display animal effects, Digging/Boost/Venom and the FinalScoring destination sentence. Complete ranges, raw-source identities and own source crops are recorded in source-reading-report.json. Page20 solo and the solo FAQ were inspected for packet completeness and excluded from candidate authority. No canonical summary, reader outputs, grades or repair history was read.

After both new gaps and the full map were complete, two targeted author passes each found zero further distinct supported rules. These are author checks, not independent saturation acceptance. The earlier draft and revision01 sealed artifacts were verified unchanged. A fresh independent saturation challenge is the next step.

Scope stays original English base v1.2 main/glossary/FAQ plus the accepted official English base IconOverview. Matching original publisher German component artwork only supplements obscured numerals already accepted; no German prose edition, strategy guide, MarineWorlds, promo, map pack, unsupplied card text or optional solo procedure is added.
'''
(HERE/'coverage-report.md').write_text(report)
names=['questions.json','answer-key.json','material-requested-facts.json','coverage-map.json','novelty-rejection-ledger.json','rejected-candidate-entries.json','shared-source-lookup-facts.json','challenge-findings-resolution.json','source-reading-report.json','validation-report.json','input-provenance.json','question-bank.md','answer-key.md','coverage-report.md','prior-artifact-immutability-check.json']
write('artifact-hashes.json',{name:digest(HERE/name) for name in names})
print('Final:131 active questions; all retained question/key objects exact;231 map records;33-page complete reading recorded;2 post-map zero passes. Prior sealed artifacts unchanged; independent challenge pending.')
