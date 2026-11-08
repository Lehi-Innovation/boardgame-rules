from pathlib import Path
import difflib
import hashlib
import json

R=Path(__file__).parent
canonical=R.parents[4]/'rules/cosmic-encounter.md'
before=canonical.read_text()
assert before==(R/'repair-freeze-04.md').read_text()
assert hashlib.sha256(before.encode()).hexdigest()=='6d41fbff548f98f3296245809fea8af488a10ffac9f9b3a7ced1ac9ec6c4762a'
replacements=[
 ('### Start Turn and hand replacement','The original rulebook lists seven encounter phases in order: **Regroup, Destiny, Launch, Alliance, Planning, Reveal, Resolution**. The first encounter also has the Start Turn step before Regroup effects.\n\n### Start Turn and hand replacement'),
 ('Aim the gate at one planet in the indicated system; put one to four of your ships in it, drawn from any combination of your existing home and foreign colonies.', 'The offense chooses one planet in the destiny-indicated system and aims the gate at it. Place one to four offense ships on the **wide end of the hyperspace gate**, drawn from any combination of the offense\'s existing home and foreign colonies.'),
 ('Each defensive ally also receives **one defender reward per ship contributed**. For each reward, draw one cosmic-deck card or retrieve one own warp ship to any own colony; combine these choices freely.', 'Each defensive ally must collect **one defender reward per ship contributed**. For each contributed ship, draw one cosmic-deck card or retrieve one own warp ship to any own colony; combine these choices freely. The ordinary rule does not permit declining these rewards.'),
 ('may play them to add to **either side\'s total**, including the opposing side.', 'may play them to add the card\'s **printed amount to either side\'s total**, including the opposing side.'),
]
after=before
for old,new in replacements:
    assert after.count(old)==1,old
    after=after.replace(old,new)
assert not (R/'repair-freeze-05.md').exists()
(R/'repair-freeze-05.md').write_text(after)
(R/'repair-freeze-05.patch').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='repair-freeze-04.md',tofile='repair-freeze-05.md')))
(R/'source-review/source-corrections-05.json').write_text(json.dumps({'basis':'Independent02 source-backed procedural proposals; proactive clarity, not a reviewer finding about an unseen summary.','source_references':['Original rulebook p7 Phases of an Encounter; p16 reference','Original rulebook p8 Launch, extraction lines619–629','Original rulebook p11 Defender Rewards, extraction lines865–875','Original rulebook p13 Reinforcement Cards, extraction lines1036–1046'],'before_sha256':hashlib.sha256(before.encode()).hexdigest(),'after_sha256':hashlib.sha256(after.encode()).hexdigest(),'replacements':[{'old':a,'new':b} for a,b in replacements],'pending_human_choices_adopted':False},indent=2,ensure_ascii=False)+'\n')
canonical.write_text(after)
core=R/'core-repair-draft.md';s=core.read_text()
for old,new in replacements:
    assert s.count(old)==1,old
    s=s.replace(old,new)
core.write_text(s)
print('repair-freeze-05',len(after),hashlib.sha256(after.encode()).hexdigest())
