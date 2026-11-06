from pathlib import Path
import hashlib,json,difflib
R=Path(__file__).resolve().parent;p=Path('/home/jonny/projects/boardgame-rules/rules/nemesis.md');src=Path('/home/jonny/projects/boardgame-rules/extracted/nemesis-rules.txt');m=json.loads((R/'input-manifest.json').read_text())
assert hashlib.sha256(src.read_bytes()).hexdigest()==m['inputs']['extracted/nemesis-rules.txt']['sha256'],'SOURCE CHANGED'
s=p.read_text();assert p.read_bytes()==(R/'original-summary.md').read_bytes(),'SUMMARY CHANGED'
s=s.replace('## Overview\n\n','## Overview\n\n**Scope:** Original Nemesis base game on the basic board, using the Captain, Pilot, Scientist, Scout, Soldier and Mechanic. This summary covers the standard semi-cooperative core. Solo, fully cooperative, playing as an Intruder, the alternative board, campaign material and expansions are excluded.\n\n',1)
s=s.replace('- **Careful Movement** (cost 2) — as Movement,','- **Careful Movement** (cost 2) — follows normal Movement restrictions, including Closed Doors blocking passage;')
s=s.replace('After resolving an Exploration token, remove it from the game (each is resolved only once, on first entry).','After resolving an Exploration token, remove it from the game into the box; it does not return to a supply or stay on the Room (each is resolved only once, on first entry).')
s=s.replace('Set the drawn token aside — it may return to the bag','Set the drawn token aside outside the bag (do not return it immediately) — it may return to the bag')
s=s.replace('a missed Melee here causes no Contamination card and no Wound.','Melee against Eggs never draws a Contamination card, whether it hits or misses, and a miss causes no Wound.')
s=s.replace('— a Noise roll is required first, and you cannot enter','— pay the Room Action cost of **2 Action cards**, and the Pod must be **Unlocked with a free Character space** in that Section. A Noise roll is required first, and you cannot enter')
s=s.replace('1. **Engines check:** reveal','1. **Engines check** (only if the ship has survived): reveal')
s=s.replace('2. **Coordinates check:** reveal','2. **Coordinates check** (only if the ship has survived): reveal')
s=s.replace('If a Scan shows INFECTED:', 'If an ordinary Scan shows INFECTED (follow the specific Action procedure; Surgery instead removes Infected cards and the Larva):')
s=s.replace('one result misses; one deals 1 Injury only if the target is a Larva or Creeper (otherwise miss); one deals 1 Injury if the target is a Larva, Creeper, or Adult (otherwise miss); one deals 1 Injury to any target; one deals 2 Injuries to any target.','a blank result misses without the Melee miss penalty; a small curled Intruder symbol deals 1 Injury only to a Larva or Creeper (otherwise miss); the larger curved Intruder symbol deals 1 Injury to a Larva, Creeper, or Adult (otherwise miss); a single hit symbol deals 1 Injury to any target; the double-hit symbol deals **2 Injuries when Shooting** to any target before Weapon modifications.')
s=s.replace('Then suffer 1 Light Wound and automatically pass, shuffling all your Action cards (hand included) into your deck.','Then suffer 1 Light Wound and automatically pass, shuffling all your cards (including the entire hand and remaining Contamination cards) into your Action deck. Your hand stays empty until the next turn.')
start=s.index('### Game modes and variants');end=s.index('## Player Reference',start)
s=s[:start]+'### Scope exclusions\n\nOptional solo and fully cooperative modes, playing as an Intruder, the alternative board and expansions are outside this standard-core reference. Their changed setup, victory and turn procedures are not used here.\n\n'+s[end:]
(R/'repair-01.patch').write_text(''.join(difflib.unified_diff(p.read_text().splitlines(True),s.splitlines(True),fromfile='original-summary.md',tofile='rules/nemesis.md')))
p.write_text(s)
print('summary repaired',len(s))
