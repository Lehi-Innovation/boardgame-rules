"""General presentation repairs after closed08; fixed regression objects unchanged."""
from pathlib import Path
import copy
import datetime
import difflib
import hashlib
import json
import shutil

B = Path(__file__).resolve().parent
ROOT = B.parents[4]
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
load = lambda p: json.loads(p.read_text())
canonical = ROOT / 'rules/spirit-island.md'
prior = B / 'source-candidate-27.md'
assert canonical.read_bytes() == prior.read_bytes()
assert H(prior) == 'ae0ad3902339bab46df46c3f860b4855df904ec661942b8e35e880e43994ec4f'
assert load(B / 'expanded-iteration-08/completed-trial-adoption.json')['trial_status'] == 'COMPLETED_DELIVERY_QUALIFIED_FACTUAL_FAILURE'
assert load(B / 'expanded08-coordinator-independent-acceptance-reference.json')['received_independent_semantic_acceptance']
bank = B / 'expanded-v24'
bank_hashes = {name: H(bank / name) for name in ['questions.json', 'answer-key.json', 'asked-fact-map.json', 'core-scope-credit.json']}
old = prior.read_text()
new = old
edits = []

def replace(label, before, after):
    global new
    assert new.count(before) == 1, label
    new = new.replace(before, after)
    edits.append({'label': label, 'before': before, 'after': after,
                  'character_delta': len(after) - len(before)})

replace(
    'Balanced layouts: keep each arrangement tied to its Spirit count',
    '1. **Island:** Randomly choose one Island Board per Spirit and join the balanced sides into the island. For one Spirit use one board. For two, any fitting arrangement is legal; the rulebook illustrates bottom-to-bottom with Oceans facing opposite outer corners. For three use the triangular layout, and for four the two-row parallelogram layout illustrated in CORE pp.6–7. [FAQ .7w4g8pg] Populate every land with its printed Invader, Dahan and Blight setup icons. Setup Blight comes from the box, never the Blight pool, and does not cascade or destroy Presence.',
    '1. **Island:** Randomly choose one Island Board per Spirit and join the balanced sides using the layout for that Spirit count. [CORE pp.6–7; FAQ .7w4g8pg]\n\n'
    '   | Spirits / boards | Balanced Island layout |\n'
    '   | --- | --- |\n'
    '   | 1 | One board. |\n'
    '   | 2 | Any fitting arrangement is legal. The rulebook shows bottom-to-bottom, with Oceans facing opposite outer corners. |\n'
    '   | 3 | Use the triangular layout illustrated in CORE p.6. |\n'
    '   | 4 | Use the two-row parallelogram layout illustrated in CORE p.7. |\n\n'
    '   Populate every land with its printed Invader, Dahan and Blight setup icons. Setup Blight comes from the box, never the Blight pool, and does not cascade or destroy Presence.'
)
replace(
    'Blighted instructions: carry the complete outcome check into the phase procedure',
    '1. **Blighted Island:** If the Blight Card is Blighted, follow its instructions at the specified timing (typically start of each Invader Phase). No such step applies with the printed no-card pool.',
    '1. **Blighted Island:** If the Blight Card is Blighted, follow its instructions at the specified timing (typically start of each Invader Phase). Finish each such action and all its triggered actions, then check victory and defeat before the next separate action. If both are met, the Spirits win a **sacrifice victory**; a loss without a win ends the game. Continue to Fear only if the game is still ongoing. No such Blighted instruction applies with the printed no-card pool. [CORE p.12; FAQ .9v5kfq7]'
)
replace(
    'Conditional Power instructions: state the available effect for each condition',
    'Its Explorer condition selects its effect: with Explorers, Push all of them; otherwise remove 1 Blight. This is not a free choice to remove Blight while Explorers remain.',
    'Its printed condition selects the available instruction: if the target has any Explorers, Push all of them and the Blight-removal instruction is **unavailable**. If it has no Explorers, instead remove 1 Blight. The player does not choose between those branches.'
)
replace(
    'Bringer: separate Fear and movement outcomes for every Invader type',
    'For each Power use, evaluate what it would destroy if resolved normally: generate **0 Fear per Explorer, 2 per Town, 5 per City**, and Push the would-be-destroyed Explorers/Towns. This special rule does not Push Cities. No real Damage is marked, so different Powers or a Repeat cannot combine their hypothetical Damage; multiple instructions **within one Power** can.',
    'For each Power use, evaluate what it would destroy if resolved normally. Apply these results separately to each would-be-destroyed Invader; the Fear result does not itself grant movement:\n\n'
    '  | Would-be-destroyed Invader | Fear | Movement from this special rule |\n'
    '  | --- | --- | --- |\n'
    '  | Explorer | 0 | Push it. |\n'
    '  | Town | 2 | Push it. |\n'
    '  | City | 5 | No Push. |\n\n'
    '  No real Damage is marked, so different Powers or a Repeat cannot combine their hypothetical Damage; multiple instructions **within one Power** can.'
)

reverse = new
for row in reversed(edits):
    assert reverse.count(row['after']) == 1
    reverse = reverse.replace(row['after'], row['before'])
assert reverse == old
assert new.split('---', 2)[:2] == old.split('---', 2)[:2]
candidate = B / 'source-candidate-28.md'
assert not candidate.exists()
candidate.write_text(new)
assert candidate.read_text() == new
canonical.write_bytes(candidate.read_bytes())
assert bank_hashes == {name: H(bank / name) for name in bank_hashes}
diff = ''.join(difflib.unified_diff(old.splitlines(True), new.splitlines(True),
                                 fromfile='source-candidate-27.md', tofile='source-candidate-28.md'))
(B / 'source-candidate-28.patch').write_text(diff)
record = {'candidate_path': str(candidate), 'candidate_sha256': H(candidate),
          'prior_candidate_sha256': H(prior), 'prior_characters': len(old),
          'candidate_characters': len(new), 'candidate_bytes': candidate.stat().st_size,
          'character_delta': len(new) - len(old), 'general_edit_count': len(edits),
          'edits': edits, 'reverse_reconstruction_exact': True,
          'YAML_unchanged': True, 'question_IDs_or_worked_case_answers_added': False,
          'new_rule_procedure_or_novelty_credit': False, 'all_four_fixed_bank_hashes_unchanged': bank_hashes,
          'source_supported_general_clarity_repair_authorized_by_coordinator': True,
          'new_full173_pair_required': True,
          'same_original_pure15_current_body_followup_required': True,
          'new_fresh_source_vote_or_whole_corpus_quota_required': False,
          'reader_generic_v15_method_unchanged': True,
          'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
(B / 'source-candidate-28-change-record.json').write_text(json.dumps(record, indent=2) + '\n')
for name in ['progress.json', 'pending-work-state.json', 'final-report-rewrite-requirements.json']:
    p = B / name
    backup = p.with_name(p.name + '.before-C28-body-change')
    assert not backup.exists()
    shutil.copyfile(p, backup)
    x = load(p)
    x['historical_C27_source15_before_C28'] = copy.deepcopy(x['source_audit'])
    source = {'status': 'PENDING_OWN_CURRENT_BODY_FOLLOWUP', 'current_PASS': False,
              'candidate_path': str(candidate), 'candidate_sha256': H(candidate),
              'agent': '/root/final_source_audit_15', 'same_initially_fresh_pure_actor': True,
              'new_fresh_vote': False, 'previous_accepted_candidate_sha256': H(prior),
              'honest_unchanged_authority_reuse_allowed': True,
              'guide_current_body_followup_not_yet_dispatched': True}
    x.update(source_audit=source, current_source_audit=copy.deepcopy(source),
             current_candidate=str(candidate), current_candidate_sha256=H(candidate),
             C28_change_record=str(B / 'source-candidate-28-change-record.json'),
             phase='C28-general-clarity-repair-own15-followup-and-new173-pair-pending',
             active_agents=[], runtime_privacy_current_verified=False,
             new_complete_reader_pair_required=True, final_reader_scores=None,
             working_report_refresh_needed_after_C28_body_change=True)
    if 'hashes' in x:
        x['hashes']['canonical_summary'] = H(candidate)
        x['hashes']['canonical_sha256'] = H(candidate)
    x['blocking_reason'] = ('C28 applies four source-supported general presentation repairs after completed08 failure. '
                            'Fixed173/506 v24 and genericv15 unchanged. Same pure15 own-current-body followup '
                            'and NEW entire173 pair are pending; no current C28 source/performance PASS claimed. '
                            'C27 and all nine completed trial outcomes remain historical. Stamp and later exact-stamped '
                            'pair/pure followup, final checks/report and explicit completion authorization remain required.')
    p.write_text(json.dumps(x, indent=2) + '\n')
print(json.dumps({k: record[k] for k in ['candidate_sha256', 'candidate_characters', 'candidate_bytes', 'character_delta', 'general_edit_count']}))
