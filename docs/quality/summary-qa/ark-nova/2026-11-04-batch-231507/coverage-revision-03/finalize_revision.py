import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
QA = HERE.parent
ROOT = QA.parents[4]
PRIOR = QA / 'coverage-revision-02'
BASE = QA / 'benchmark-v1.2'

def read(path):
    return json.loads(path.read_text())

def write(name, obj):
    (HERE / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

q = read(HERE / 'questions.json')['questions']
a = read(HERE / 'answer-key.json')['answers']
f = read(HERE / 'material-requested-facts.json')
m = read(HERE / 'coverage-map.json')
q0 = read(PRIOR / 'questions.json')['questions']
a0 = read(PRIOR / 'answer-key.json')['answers']
f0 = read(PRIOR / 'material-requested-facts.json')
m0 = read(PRIOR / 'coverage-map.json')
bq = read(BASE / 'questions.json')['questions']
ba = read(BASE / 'answer-key.json')['answers']
adjud = read(QA / 'novelty-adjudication-04/report.json')
retired = set(adjud['retire_ids'])
active = {r['id'] for r in q}
qd = {r['id']: r for r in q}
ad = {r['id']: r for r in a}
oldq = {r['id']: r for r in q0}
olda = {r['id']: r for r in a0}

assert len(q) == len(a) == len(f) == 95
assert [r['id'] for r in q] == [r['id'] for r in a]
assert active == set(f) == set(adjud['surviving_input_ids']) | {'Q140'}
assert q[:20] == bq and a[:20] == ba
assert all(ad[r['id']] == r for r in a0[:20] if r['id'] != 'Q17')
assert all(qd[x] == oldq[x] and ad[x] == olda[x] for x in active - {'Q17', 'Q140'})
assert all(f[x] == f0[x] for x in active - {'Q17', 'Q140'})
assert all(qd[x] == oldq[x] and ad[x] == olda[x] for x in ['Q06', 'Q42'])
assert len(retired) == 37 and retired.isdisjoint(active)
assert all(x in active for x in ['Q70', 'Q72', 'Q96', 'Q100'])
assert len(m['passages']) == len({r['passage_id'] for r in m['passages']}) == 232
assert {r['passage_id'] for r in m0['passages']} <= {r['passage_id'] for r in m['passages']}
assert active <= {x for r in m['passages'] for x in r['question_ids']}

edge_keys = {'question_ids', 'covered_by', 'procedure_covered_by', 'procedure_covered_by_active_ids', 'active_procedure_covering_ids'}
edge_count = 0
def verify_edges(obj):
    global edge_count
    if isinstance(obj, list):
        for v in obj:
            verify_edges(v)
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if k in edge_keys and isinstance(v, list):
                assert set(v) <= active, (k, v)
                edge_count += len(v)
            else:
                verify_edges(v)

verify_edges(m)
remap = read(HERE / 'transitive-retirement-map.json')
assert set(remap) == retired
assert all(set(ids) <= active and ids for ids in remap.values())
archive = read(HERE / 'rejected-candidate-entries.json')['new_retirements']
assert {r['id'] for r in archive} == retired
for r in archive:
    x = r['id']
    assert r['historical_question'] == oldq[x]
    assert r['historical_answer'] == olda[x]
    assert r['historical_material_fact_entry'] == f0[x]
lookups = read(HERE / 'shared-source-lookup-facts.json')
for r in lookups:
    if r.get('retired_id') in retired:
        assert r['all_printed_or_contextual_facts_preserved'] == f0[r['retired_id']]['material_requested_facts']
assert len([p for p in m['passages'] if p['passage_id'].startswith('GSP.')]) == 64
byid = {p['passage_id']: p for p in m['passages']}
for x in ['GAB.constriction', 'GAB.hypnosis', 'GAB.pilfering_targets', 'GAB.venom']:
    assert {'Q39', 'Q125'} <= set(byid[x]['question_ids'])

immut = read(HERE / 'prior-artifact-immutability-check.json')
prior_count = 0
for folder, entries in immut.items():
    for filename, rec in entries.items():
        observed = sha(QA / folder / filename)
        assert observed == rec['sealed_sha256'] == rec['observed_sha256']
        assert rec['unchanged']
        prior_count += 1

closure = [
    {'pass': 2, 'addition_count': 0, 'new_ids': [],
     'target': 'After the complete 232-record map: normal gameplay, SC01/SC02 priority and bands, four interaction-target edges, Digging choices and compaction, and retained F01–F03 source facts.',
     'result': 'No additional distinct procedure, consequential timing, exception or outcome branch identified. Exact printed Species Diversity and income tables remain lookup evidence; Q137 retains empty-face/once-only placement procedure.',
     'complete_source_map_preceded_pass': True},
    {'pass': 3, 'addition_count': 0, 'new_ids': [],
     'target': 'Final source-to-active-prompt sweep across all 33 PDF pages: setup/ordinary play, five actions, tracks/diagrams, break/endgame, all glossary abilities and listed sponsors, final-scoring clarifiers, advanced maps, every base FAQ restriction and the full icon overview.',
     'result': 'No further source-supported distinct procedure remains unasked. Parameter, named-icon, amount and whole-table substitutions are retained as lookup facts without new standalone credit. All live map edges and transitive retirement destinations rechecked.',
     'complete_source_map_preceded_pass': True}
]
ledger = read(HERE / 'novelty-rejection-ledger.json')
assert len(ledger['accepted_candidates']) == 75
ledger['closure_passes'] = closure
ledger['terminal_zero_addition_passes'] = 2
ledger['next_step'] = 'Sealed author candidate ready for fresh independent saturation challenge; author closure is not independent acceptance.'
write('novelty-rejection-ledger.json', ledger)

reread = read(HERE / 'provisional-source-reread.json')
reread['status'] = 'Complete 33-page native source reread and primary-render reinspection; final adjudication applied; two terminal zero-addition author passes complete.'
reread['visual_reinspection'] = {'main_pdf_pages': 20, 'glossary_pdf_pages': 8, 'faq_pdf_pages': 3, 'icon_overview_pages': 2,
    'renders': '../coverage-revision-02/*-pages-*.jpg (unchanged direct primary-PDF renders)',
    'fresh_precision_crops': ['primary-random-start.png', 'primary-normal-turns.png', 'primary-mandatory-special-priority.png']}
reread['terminal_author_passes'] = closure
reread['scope'] = 'Original English base v1.2; solo passages read but excluded, no Marine Worlds or strategy-guide authority.'
write('source-reading-report.json', reread)

validation = {'status': 'pass', 'active_questions': 95, 'highest_historical_id': 'Q140', 'baseline_questions': 20,
    'accepted_additions_above_baseline': 75, 'current_retirements': 37, 'total_historical_retirements': len(ledger['all_rejected_historical_ids']),
    'source_passage_records': 232, 'sponsor_map_records_including_explicit_223_absence': 64,
    'live_map_edge_occurrences_checked': edge_count, 'prior_sealed_artifacts_unchanged': prior_count,
    'original20_question_objects_exact_benchmark_v1_2': True, 'original20_key_objects_exact_benchmark_v1_2': True,
    'original19_keys_other_than_Q17_unchanged': True, 'Q17_exact_SC01_SC02_baseline': True,
    'Q06_Q42_question_and_key_objects_unchanged': True, 'other_surviving_question_key_and_fact_objects_unchanged': True,
    'all_37_full_historical_entries_and_material_facts_preserved': True, 'all_37_transitive_targets_live': True,
    'all_prior_231_passage_ids_preserved': True, 'no_dead_question_edges_in_live_map_or_lookup': True,
    'GAB_four_targeting_precision_repairs': True, 'terminal_author_zero_addition_passes': 2,
    'independent_final_saturation': 'pending coordinator challenge; not claimed by author'}
write('validation-report.json', validation)

nd = read(HERE / 'independent-novelty-decisions.json')
nd['report_sha256'] = sha(QA / 'novelty-adjudication-04/report.json')
assert nd['retire_ids'] == adjud['retire_ids'] and nd['decisions'] == adjud['decisions']
write('independent-novelty-decisions.json', nd)

inputs = []
for path in [BASE/'questions.json', BASE/'answer-key.json', QA/'source-key-correction-SC01.json', QA/'source-key-clarification-SC02.json',
             QA/'coverage-challenge-03/report.json', QA/'novelty-adjudication-04/report.json',
             PRIOR/'questions.json', PRIOR/'answer-key.json', PRIOR/'coverage-map.json', PRIOR/'material-requested-facts.json']:
    inputs.append({'path': str(path.relative_to(QA)), 'sha256': sha(path)})
write('input-provenance.json', {'role': 'Source-only author; no canonical summary, reader outputs or grades consulted.',
    'baseline': 'benchmark-v1.2; original20 questions unchanged, SC01+SC02 versioned Q17 only', 'inputs': inputs,
    'primary_pdf_sources': reread['pdfs'],
    'supplementary_numeric_component_art': {'accepted_primary': '../table-source-check/Spielzene.jpg and Back_arche_nova.jpg; original German publisher-printed component art, Animals II numeric cells only',
       'scope_boundary': 'English original base prose remains controlling; no German rules edition adopted.',
       'corroborating_only': 'ark-nova-original-physical-animals-II.png is a coordinator-supplied third-party 2022 review photograph of the original German card, not user firsthand and not an English card.',
       'source_reports': ['../table-source-check/followup-source-report.json', '../table-source-check/reputation-map-source-report.json', '../table-source-check/evidence-manifest.json']},
    'excluded': ['strategy guide authority', 'Marine Worlds', 'solo rules as question authority', 'canonical summary', 'reader outputs', 'grades'],
    'immutable_prior_artifact_count': prior_count})

question_text = ['# Ark Nova original base — revision 03 question bank', '', '95 active stable IDs through Q140. Original20 question objects unchanged. Retired IDs are archived and never reused.', '']
answer_text = ['# Ark Nova original base — revision 03 answer key', '', 'Source-only authored key. Q17 inherits the explicitly versioned benchmark-v1.2 SC01/SC02 clarification; all other retained answers are unchanged.', '']
for r in q:
    x = r['id']
    question_text += [f'## {x}', '', r['question'], '']
    ans = ad[x]
    answer_text += [f'## {x}', '', r['question'], '', ans['expected_answer'], '', 'Material requested facts:', '']
    answer_text += ['- ' + str(v) for v in f[x]['material_requested_facts']]
    answer_text += ['', 'Primary source references:', '']
    answer_text += ['- ' + (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)) for v in ans['source_references']]
    answer_text += ['']
(HERE/'question-bank.md').write_text('\n'.join(question_text))
(HERE/'answer-key.md').write_text('\n'.join(answer_text))

(HERE/'coverage-report.md').write_text('''# Ark Nova source coverage revision 03

The sealed author candidate has 95 active stable IDs through Q140 and 232 source-passage records. It retains all original20 question objects exactly, and inherits all20 answer objects from benchmark-v1.2. The only baseline key change is explicitly versioned Q17: SC01 corrects the depicted size bands, while SC02 clarifies mandatory removal of eligible special-enclosure tokens before standard-enclosure fallback. Historical key versions and source evidence are retained in source-key-corrections.json.

Q140 adds the previously missing normal-gameplay cluster: random starting player, clockwise turns, no formal rounds, and one ordinary action with possible effects or bonuses (Main pp5–6). The final independent novelty adjudication retires37 additional standalone questions. Full question/key/fact entries and exact printed lookup data remain in rejected-candidate-entries.json and shared-source-lookup-facts.json. All retirement destinations resolve transitively to surviving prompts. Such references cover shared procedures; they do not claim an earlier prompt literally asks every printed number. Q70, Q72, Q96 and Q100 retain distinct optional placement, actual tuck/sale choices, and required border-placement procedures. No question was removed on reader-performance grounds.

Four interaction source records now explicitly include Q39 and Q125 for targeting and eligibility precision. The F01–F03 resolutions remain mapped: Species Diversity category counting/table and the full income table are preserved as source lookup; Q137 still asks standard-empty-face and once-only covered-bonus procedure. The earlier Digging-choice and ordered-compaction questions remain unchanged. Q06 and Q42 remain exact.

The complete primary packet was reread: 20 main-rule pages, eight glossary pages, three FAQ pages and two official base Icon Overview pages. The map includes setup, component diagrams and tracks, every base procedural main-rule passage, every listed individual sponsor, final-scoring clarifiers, advanced-map passages, all base FAQ restrictions, and the complete official Icon Overview. Solo text was read for scope classification and excluded from question authority. Map3 has no additional printed clarification in this packet; Sponsor223 is absent. Individual deck cards beyond text printed in the supplied packet are not inferred.

Original German publisher component photographs supplement only Animals II numeric art obscured in the English PDF. The English base prose remains controlling. The file ark-nova-original-physical-animals-II.png is a coordinator-supplied third-party2022 review photograph of the original German card; it is corroborating research history, not user-firsthand or English-card evidence. No strategy-guide authority or Marine Worlds material was adopted.

Two terminal author passes after the complete final map found zero additional distinct procedures. These are author closure checks, not independent saturation acceptance. The fresh coordinator challenge is pending. validation-report.json records exact retained-object preservation, all live coverage edges, all full retirement archives, and unchanged hashes for37 earlier sealed artifacts. No canonical summary, reader outputs or grades were consulted.
''')

(HERE/'author-prompt-provenance.md').write_text('''# Author instruction provenance — revision 03

Coordinator task (preserved wording):

> Continue authorized source-only author role. New report coverage-challenge-03/report.json found missing normal-gameplay/startplayer Q140 and27 standalone novelty rejections, 4 map precision repairs and Q17 mandatorypriority wording. Root created benchmark-v1.2 with explicitSC02 mandatoryQ17; source-key-clarification-SC02.json preserves prior keys. Prepare coverage-revision-03 ONLY, don't touch prior drafts. A new fresh novelty-adjudication-04 agent is now independently deciding27+Q81; wait its report before finalizing IDs (can do source reread/newQ140/mapping preparation now). Latest coordinator overrides prior informal distinction: whole CORE tables do NOT themselves grant novelty if actualprocedure already asked; preserve printeddata aslookup, don'tinflateN. Expect retirement of27+possibleQ81 except supported independentcontrarydecision. Preserve stableIDs and original20questions byte/objectequivalent; original19keys unchanged, Q17 exactlybenchmark-v1.2. Update requestedfactsQ17 fromprefer tomandatory, provenanceSC01+SC02 explicit. Remap all archived IDs transitively to actualsurviving prompts (e.gQ64->Q62 retired, Q79->Q76 retired); lookupfacts preserved. Fix GAB targetingedges Q39/Q125 asreport. Add Q140 exact missing randomstartingplayer/clockwise/noformalrounds/oneactionplusbonuses cluster withsources. Record allreportdecisions, no readerfailuresexist; retireonlypre-reader novelty. After final decisions rebuildcomplete231+passagemap, fullsource reread and two terminalzeroaddpasses, full exactobject/hashpreservation, neutral evidence. Allwriteundercoverage-revision-03 only, no summary/readers/grades. Notify when provisionalprepared then wait adjudicationreport and finalize. Follow roleblindness, no oldsummary.

Final coordinator direction (supersedes provisional messages):

> Saved adjudication report now at novelty-adjudication-04/report.json. FINAL correction supersedesprovisional: KEEPQ70 (optionalordinaryfreeplacement differsmandatoryunique Q35 andrequiredregularBuild Q08); retire37total exactlyreport['retire_ids'];94rev02survivors+Q140=>95active. Please readallfinaldecisions and transitively remap toliveIDs, preserveactuallookupfactswithoutclaimingliteral earlierpromptrequestsallnumbers. Completefinalrev03 mapping/twozeroaddpasses + checks asassigned. ReportminorSC01/SC02labelbeingcorrectedbyadjudicator onlyprovenance. No moreindependentnoveltyinputs pending; finalizer nowproceed.

The prior original author prompt and intervening revision prompts remain immutable in coverage-draft/author-prompt-provenance.md, coverage-revision-01/author-prompt-provenance.md and coverage-revision-02/author-prompt-provenance.md. This revision reads only authorized source and bank/adjudication artifacts. It does not claim an independent author audit.
''')

exclude = {'artifact-hashes.json', 'sealed-manifest.json'}
hashes = {p.name: sha(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name not in exclude}
write('artifact-hashes.json', hashes)
core = ['questions.json', 'answer-key.json', 'material-requested-facts.json', 'coverage-map.json', 'novelty-rejection-ledger.json', 'question-bank.md', 'answer-key.md', 'validation-report.json']
write('sealed-manifest.json', {'status': 'sealed_author_candidate_for_fresh_independent_challenge', 'revision': 'coverage-revision-03',
    'active_question_count': 95, 'highest_historical_id': 'Q140', 'source_passage_records': 232,
    'new_question_ids': ['Q140'], 'current_retired_count': 37, 'retired_ids': sorted(retired, key=lambda x: int(x[1:])),
    'baseline': 'benchmark-v1.2 (SC01+SC02)', 'terminal_author_zero_addition_passes': 2,
    'independent_saturation_accepted': False, 'core_sha256': {x: hashes[x] for x in core},
    'all_artifact_hashes_sha256': sha(HERE/'artifact-hashes.json')})
print(json.dumps({'counts': validation, 'sealed_manifest_sha256': sha(HERE/'sealed-manifest.json'), 'core_sha256': {x: hashes[x] for x in core}}, indent=2))
