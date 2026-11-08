"""Prepare a general clarity proposal; do not mutate the canonical guide."""
from pathlib import Path
import difflib
import hashlib
import json

B = Path(__file__).resolve().parent
ROOT = B.parents[4]
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
prior = B / 'source-candidate-28.md'
assert H(prior) == H(ROOT / 'rules/spirit-island.md') == '8f17f3ce025a16045709c4302e1c2e46d9da22c1e705fc4db28d8b7182985e5c'
original = prior.read_text()
text = original
changes = []

def replace(label, old, new):
    global text
    assert text.count(old) == 1, label
    text = text.replace(old, new)
    changes.append({'general_clarity_change': label, 'old': old, 'new': new,
                    'character_delta': len(new) - len(old)})

replace(
    'Keep each operation’s survival effect and destruction-Fear consequence together',
    '| Instruction | Effect on the piece |\n'
    '| --- | --- |\n'
    '| **Damage** | Mark Damage; reaching Health destroys the piece immediately. |\n'
    '| **Destroy** | Return the specified piece to supply regardless of Health or marked Damage. |\n'
    '| **Remove** | Take the specified piece off the board without a Damage-to-Health test. |\n'
    '| **Replace** | Remove the original piece and put the specified new piece in its place, retaining marked Damage. |',
    '| Instruction | Effect on the piece | Destruction Fear |\n'
    '| --- | --- | --- |\n'
    '| **Damage** | Mark Damage; reaching Health destroys the piece immediately. | If this destroys a Town/City, gain 1/2 Fear respectively, in addition to explicit Fear. |\n'
    '| **Destroy** | Return the specified piece to supply regardless of Health or marked Damage. | A Town/City generates 1/2 Fear respectively, in addition to explicit Fear. |\n'
    '| **Remove** | Take the specified piece off the board without a Damage-to-Health test. | None from removal; explicit Fear still applies. |\n'
    '| **Replace** | Remove the original piece and put the specified new piece in its place, retaining marked Damage. | None from replacement itself. If retained Damage destroys the new Town/City, gain 1/2 Fear respectively, in addition to explicit Fear. |',
)
replace(
    'Present Fear generation as a sequential refill loop with immediate divider timing',
    'Fear is island-wide. For each Fear, move one marker from the Fear Pool to Generated Fear. When all **4 per Spirit** markers have moved, earn the top Fear Card face-down, return all markers to the pool and continue with any leftover Fear toward the next card. If earning a card exposes a Terror divider, the new Terror Level applies immediately; its victory condition can end the game at the outcome check. Earning the final card reveals Victory; its text never needs resolving.',
    'Fear is island-wide. Process generated Fear **one point at a time**:\n\n'
    '1. Move one marker from the Fear Pool to Generated Fear.\n'
    '2. As soon as Generated Fear holds all **4 per Spirit** markers, earn the top Fear Card face-down. Apply any newly exposed Terror Level immediately, then return all markers to the Fear Pool **before processing the next point**.\n'
    '3. Repeat for every remaining point of Fear, continuing toward the next card after each refill.\n\n'
    'A newly exposed Terror Level changes the victory condition immediately; the game can end at the outcome check. Earning the final card reveals Victory; its text never needs resolving.',
)
replace(
    'Attach ownership to the lost Presence while keeping the Dahan trigger unrestricted',
    "- **Thunderspeaker:** Presence may accompany each moved Dahan, including generic Move as well as Gather/Push; two Dahan can carry two Presence. **Sworn to Victory** triggers after an entire single-land Ravage for each Dahan destroyed there: destroy one of Thunderspeaker's Presence within Range 1 per Dahan, even if no Blight was added. Finish the Ravage, cascades and counterattack before this triggered loss. [Core: .bu6oc6l, .bu6oc73, .bu6ofsi]",
    "- **Thunderspeaker:** Presence may accompany each moved Dahan, including generic Move as well as Gather/Push; two Dahan can carry two Presence. **Sworn to Victory:** finish the entire single-land Ravage, including Blight, cascades and counterattack, then count every Dahan destroyed in that Ravage. **For each destroyed Dahan, Thunderspeaker destroys one of its own Presence within Range 1 of the Ravaged land**, even if no Blight was added. [Core: .bu6oc6l, .bu6oc73, .bu6ofsi]",
)
replace(
    'Keep Bringer’s per-piece Fear and movement beside its per-use accumulation rule',
    '  No real Damage is marked, so different Powers or a Repeat cannot combine their hypothetical Damage; multiple instructions **within one Power** can.',
    '  For each Invader that this Power use would destroy, gain **0/2/5 Fear for an Explorer/Town/City**, respectively; Push only the Explorer or Town. No real Damage is marked, so different Powers or a Repeat cannot combine their hypothetical Damage; multiple instructions **within one Power** can.',
)
assert len(changes) == 4
assert text.split('---', 2)[:2] == original.split('---', 2)[:2]
assert not any(f'Q{n}' in text for n in range(1, 174))
proposal = B / 'source-candidate-29-proposed-not-applied.md'
patch = B / 'source-candidate-29-proposed.patch'
record = B / 'source-candidate-29-proposed-change-record.json'
assert not any(p.exists() for p in [proposal, patch, record])
proposal.write_text(text)
patch.write_text(''.join(difflib.unified_diff(original.splitlines(True), text.splitlines(True), fromfile='source-candidate-28.md', tofile='source-candidate-29-proposed-not-applied.md')))
bank = B / 'expanded-v24'
record.write_text(json.dumps({
    'proposal_only_canonical_unchanged': True,
    'coordinator_authorization': 'expanded09-coordinator-independent-acceptance-reference.json',
    'prior_sha256': H(prior), 'proposed_sha256': H(proposal),
    'prior_characters': len(original), 'proposed_characters': len(text),
    'character_delta': len(text) - len(original), 'changes': changes,
    'YAML_unchanged': True, 'new_procedures_or_novelty_credit': 0,
    'no_question_ids_or_worked_numeric_benchmark_cases_added': True,
    'bank_unchanged': {n: H(bank / n) for n in ['questions.json', 'answer-key.json', 'asked-fact-map.json', 'core-scope-credit.json']},
    'same_pure_own_current_body_followup_and_NEW_full173_pair_required_after_apply': True,
    'new_corpus_native_or_coverage_quota': False,
    'parent_full_diff_review_pending': True,
}, indent=2, ensure_ascii=False) + '\n')
assert H(ROOT / 'rules/spirit-island.md') == H(prior)
print(json.dumps({'proposal_sha256': H(proposal), 'characters': len(text), 'bytes': proposal.stat().st_size,
                  'delta': len(text)-len(original), 'patch_characters': len(patch.read_text()),
                  'record_characters': len(record.read_text()), 'canonical_unchanged': True}))
