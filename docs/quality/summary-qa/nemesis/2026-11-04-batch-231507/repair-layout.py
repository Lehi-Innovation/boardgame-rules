from pathlib import Path
import difflib
R=Path(__file__).resolve().parent;p=Path('rules/nemesis.md');old=p.read_text();s=old
start=s.index('### Escape Pods\n');end=s.index('### Self-Destruct sequence',start)
s=s[:start]+'''### Escape Pods

- **Unlock:** all Pods begin Locked. Unlock manually through Items/Hatch Control, or automatically on the first Character death or Self-Destruct's first yellow space.
- **Board:** pay 2 Action cards for the corresponding Evacuation Section A/B Room Action. A Pod there must be Unlocked with a free Character space. No entry while the Section contains an Intruder or Malfunction. First roll Noise; an Intruder appearing or reaching the Section makes entry fail.
- **Capacity:** 2 Characters per Pod. Heavy Objects take no Character space.
- **Launch immediately:** after boarding you may launch. Remove the Pod token and its occupants' miniatures from the game; they stop participating and count as arriving on Earth. They still face the final Contamination and Objective checks.
- **Wait after boarding:** you pass the current turn. You remain treated as present in the Section for Noise rolls from bag development (FAQ Rules 1).
- **At the start of your first round in each later Player Phase**, choose exactly one: remain waiting and pass; launch; or exit for free into the corresponding Section Room and play a full round of 2 Actions (FAQ Rules 2).
- **A second Character boards your waiting Pod:** that Character may launch it immediately with both of you aboard; the first occupant has no reserved launch control.
- **An Intruder appears in the Section while you wait:** all Characters in that Section's Pods immediately return to its Room.
- **A Malfunction appears in the Section while you wait:** you may still wait, launch or exit; the marker blocks only new entry to Pods (FAQ Rules 3).

'''+s[end:]
start=s.index('**Intruder Injuries and death:**');end=s.index('**Intruder Retreat:**',start)
s=s[:start]+'''**Intruder Injuries and death:** after any Injuries, put that many Injury markers on the Intruder's base and check its Injury Effect. Compare **current total Injuries**, not just the latest hit.

| Target | Injury Effect | On death |
|---|---|---|
| Larva | 1 Injury kills | Remove miniature; no Carcass |
| Egg | 1 Injury destroys | Remove Egg |
| Creeper | Draw 1 Intruder Attack card; use only its blood value. Blood ≤ Injuries kills; higher means alive. | Remove miniature; place Carcass in Room |
| Adult | Draw 1 Intruder Attack card; use only its blood value. Blood ≤ Injuries kills; higher means alive. | Remove miniature; place Carcass in Room |
| Breeder | Draw 2 Attack cards and sum blood values. Sum ≤ Injuries kills; higher means alive. | Remove miniature; place Carcass in Room |
| Queen | Draw 2 Attack cards and sum blood values. Sum ≤ Injuries kills; higher means alive. | Remove miniature; place Carcass in Room |

The blood value can change at each check. Two Five Injuries tokens help track larger totals. Any Retreat arrow changes the check to the retreat procedure below.

'''+s[end:]
(R/'repair-08-layout.patch').write_text(''.join(difflib.unified_diff(old.splitlines(True),s.splitlines(True),fromfile='prose-procedures',tofile='structured-procedures')));p.write_text(s)
