from pathlib import Path
import difflib
import hashlib
import json

R = Path(__file__).parent
canonical = R.parents[4] / 'rules/cosmic-encounter.md'
before = canonical.read_text()
assert hashlib.sha256(before.encode()).hexdigest() == 'd816b4020aa1a0f75b055342bb643bcc7cfe92945fe1750384b5b00cf4b79d7a'
assert before == (R/'repair-freeze-03.md').read_text()
replacements = [
 ('Wild becomes available while the power is zapped.', 'Only Wild is available for an otherwise legal play while the power is zapped. Zapping the enabled power does not undo the already-played flare or permit a second play of it in the same encounter; the ordinary per-player and per-flare limits still apply.'),
 ('“Sent” ships can be lost through a separate effect, including voluntary sends, without being encounter-losing ships.', '“Sent” ships reach the warp through a specific action or effect, sometimes voluntarily, while not directly involved in the encounter; they count as lost rather than encounter-losing ships.'),
 ('With Mobius Tubes and no colony to receive released ships,', 'Ships landing on colonies do so simultaneously, including ships released by Mobius Tubes (FAQ p19, general landing rule). With Mobius Tubes and no colony to receive released ships,'),
 ('Reserve Wild need only be played once in the encounter, then can take eligible reinforcement discards for its remainder.', 'Reserve Wild need only be played once in the encounter. For the remainder of that encounter, whenever another player discards a reinforcement, its user may take that card into their own hand; this does not retrieve their own discards.'),
]
after = before
for old, new in replacements:
    assert after.count(old) == 1, old
    after = after.replace(old, new)
freeze = R/'repair-freeze-04.md'
assert not freeze.exists()
freeze.write_text(after)
(R/'repair-freeze-04.patch').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='repair-freeze-03.md',tofile='repair-freeze-04.md')))
(R/'source-review/source-corrections-04.json').write_text(json.dumps({'basis':'Independent source/key review CKS-03/04/05/06', 'before_sha256':hashlib.sha256(before.encode()).hexdigest(),'after_sha256':hashlib.sha256(after.encode()).hexdigest(),'replacements':[{'old':a,'new':b} for a,b in replacements], 'sources':['2018 FAQ p19 Reserve Wild, extraction lines1784–1789','2018 FAQ p19 general landing statement with Mobius example, extraction lines1796–1797','Original rulebook p13 flare limits and FAQ p6 power-enabled Super use, extraction lines525–537/578–581','2018 FAQ p3 losing/lost/sent categories, extraction lines205–220'], 'pending_human_choices_adopted':False},indent=2,ensure_ascii=False)+'\n')
canonical.write_text(after)
# Keep editable authoring inputs in sync without replacing any historical freeze.
core = R/'core-repair-draft.md'
s = core.read_text()
for old,new in replacements[:2]:
    assert s.count(old)==1
    s=s.replace(old,new)
core.write_text(s)
assembly = R/'assemble_repair.py'
s = assembly.read_text()
for old,new in replacements[2:]:
    assert s.count(old)==1
    s=s.replace(old,new)
assembly.write_text(s)
print('repair-freeze-04',len(after),hashlib.sha256(after.encode()).hexdigest())
