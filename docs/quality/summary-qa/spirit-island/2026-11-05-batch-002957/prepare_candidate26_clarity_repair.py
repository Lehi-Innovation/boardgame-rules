from pathlib import Path
import difflib
import hashlib
import json

B = Path(__file__).resolve().parent
ROOT = B.parents[4]
P = ROOT / 'rules/spirit-island.md'
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
HS = lambda s: hashlib.sha256(s.encode()).hexdigest()
load = lambda p: json.loads(p.read_text())
assert H(P) == H(B / 'source-candidate-25.md') == 'f0297380795b0939b0480cb52d97499a5d611b57a8243d5a56820099979727b6'
assert load(B / 'expanded-iteration-06/completed-trial-adoption.json')['trial_status'] == 'COMPLETED_DELIVERY_QUALIFIED_FACTUAL_FAILURE'
old = P.read_text()
changes = [
    ('presence_local_count',
     '1. Destroy **one Presence from each Spirit** with Presence there, not every disk and not just one disk total.',
     '1. Destroy **one Presence from each Spirit** with Presence there, not every disk and not just one disk total. Decrease each affected Spirit\'s Presence count in that land by exactly one.',
     ['core_blight']),
    ('gain_does_not_resolve',
     'Gaining during Growth allows playing that card in the later play/pay step; gaining it mid-turn does not by itself let you play it.',
     'Gaining during Growth allows playing that card in the later play/pay step; gaining it mid-turn does not by itself let you play it. Gaining a card does not itself resolve that card\'s effects.',
     ['core_gain', 'faq_play_resolution']),
    ('land_order_outcome',
     'Do not finish Ravages in all other lands first.',
     'Do not finish Ravages in all other lands first. Players may choose which qualifying land Ravages first; a win at that land\'s completed action-tree check ends the game before any later Ravage.',
     ['faq_outcome']),
]
core = ROOT / 'extracted/spirit-island-rules.txt'
faq = ROOT / 'docs/quality/summary-qa/batches/2026-11-05-batch-002957/source-preflight/spirit-island/living-faq-core-game.txt'
sources = {}
for name, path, start, end, first, last in [
    ('core_blight', core, 38000, 42000, 'After Setup, whenever you add Blight to a land', '(For an example Ravage Phase'),
    ('core_gain', core, 47500, 51500, 'GAINING POWER CARDS', 'POWER AND FEAR EFFECTS'),
    ('faq_play_resolution', faq, 54500, 60000, 'When an effect lets a Spirit play a Power Card outside of the Spirit Phase', 'How do I figure out the Difficulty'),
    ('faq_outcome', faq, 54500, 60000, 'What creates a sacrifice victory?', 'How do you score a sacrifice victory?'),
]:
    text = path.read_text()
    a = text.index(first, start, end)
    z = text.index(last, a, end)
    sources[name] = {'path': str(path), 'full_sha256': H(path), 'range': [a, z], 'literal_passage': text[a:z], 'passage_sha256': HS(text[a:z]), 'actual_parent_full_window_read': {'range': [start, end], 'slice_sha256': HS(text[start:end]), 'output_cap_tokens': 4000, 'truncated': False, 'one_literal_range_per_notify_event': True}}
new = old
for name, before, after, refs in changes:
    assert new.count(before) == 1 and before != after
    new = new.replace(before, after)
assert new.split('---', 2)[1] == old.split('---', 2)[1]
back = new
for _, before, after, _ in reversed(changes):
    assert back.count(after) == 1
    back = back.replace(after, before)
assert back == old
bank_names = ['questions.json', 'answer-key.json', 'asked-fact-map.json', 'core-scope-credit.json']
bank = {name: H(B / 'expanded-v24' / name) for name in bank_names}
candidate = B / 'source-candidate-26.md'
assert not candidate.exists()
candidate.write_text(new)
P.write_text(new)
assert candidate.read_bytes() == P.read_bytes()
assert bank == {name: H(B / 'expanded-v24' / name) for name in bank_names}
record = {
    'candidate': str(candidate), 'candidate_sha256': H(candidate), 'canonical_sha256': H(P),
    'previous_candidate_sha256': H(B / 'source-candidate-25.md'),
    'characters': len(new), 'bytes': candidate.stat().st_size,
    'change_count': len(changes), 'changes': [{'id': n, 'old': a, 'new': z, 'primary_source_citations': refs} for n, a, z, refs in changes],
    'added_characters': len(new) - len(old), 'exact_reverse_reconstruction_PASS': True,
    'yaml_unchanged': True, 'new_rule_or_procedure_claimed': False, 'new_novelty_credit': 0,
    'bespoke_question_ids_or_case_number_answers_added': False,
    'bank_key_map_scope_bytes_unchanged': bank,
    'no_reader_resampling_or_threshold_change': True,
    'new_fresh_pure_source_audit_and_full173_pair_mandatory': True,
    'source14_C25_PASS_historical_only_after_body_change': True,
}
(B / 'source-candidate-26-change-record.json').write_text(json.dumps(record, indent=2, ensure_ascii=False) + '\n')
(B / 'source-candidate-26-clarity-primary-evidence.json').write_text(json.dumps(sources, indent=2, ensure_ascii=False) + '\n')
(B / 'source-candidate-26-changes.patch').write_text(''.join(difflib.unified_diff(old.splitlines(True), new.splitlines(True), fromfile='source-candidate-25.md', tofile='source-candidate-26.md')))
print(json.dumps({'candidate_sha256': H(candidate), 'characters': len(new), 'bytes': candidate.stat().st_size, 'added_characters': len(new)-len(old), 'changes': len(changes)}))
