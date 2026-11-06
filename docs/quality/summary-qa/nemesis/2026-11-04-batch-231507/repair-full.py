from pathlib import Path
import difflib
R=Path(__file__).resolve().parent;p=Path('rules/nemesis.md');old=p.read_text();s=old
start=s.index('### Discard piles\n');end=s.index('## Turn Structure',start)
s=s[:start]+'''### Discard piles

Normal discards are face up; each deck has its own discard space:

| Component | Destination |
|---|---|
| Used/discarded Action cards | That Character's Action discard pile |
| Gained Contamination cards | On top of that Character's Action discard pile; never paid as Action costs |
| Discarded Item cards | Matching Item discard pile |
| Discarded Event cards | Event discard pile |
| Discarded Intruder Attack cards | Intruder Attack discard pile |
| Discarded Serious Wound cards | Serious Wound discard pile |
| Discarded markers | Appropriate marker pool |

An explicit effect can give a different destination: Search and Storage keep one of two Item cards and return the other face down to the bottom of the chosen deck. Removed-from-game Contamination and Exploration tokens do not return to their supplies.

'''+s[end:]
s=s.replace('**Fire Damage** — each Intruder in a Room with a Fire marker suffers 1 Injury.','**Fire Damage** — each Intruder in a Room with a Fire marker suffers 1 Injury. Apply Injury markers and the normal Injury Effect check immediately (including possible death or retreat). This happens after Intruder Attacks and before the Event card.')
s=s.replace('**Breeder** — same as Adult: all players roll for Noise in order (skip players in Combat). Return the token to the bag.','**Breeder** — all players roll for Noise in order (skip players in Combat), then return the Breeder token as instructed by the manual. The FAQ explicitly specifies immediate pre-roll return for an Adult; do not silently extend that timing clarification to another token type.')
s=s.replace('- **Shoot** — attack an Intruder in your Room with a Weapon in your Hand, discarding 1 Ammo from that Weapon\'s card.','- **Shoot** (cost 1 Action card + 1 Ammo) — attack an Intruder in your Room with a Weapon in your Hand, discarding 1 Ammo from that Weapon\'s card.')
s=s.replace('- **Pick Up Heavy Object** — pick up 1 Heavy Object in your Room (Character Corpse, Intruder Carcass, or Intruder Egg).','- **Pick Up Heavy Object** (cost 1 Action card) — pick up 1 Heavy Object in your Room (Character Corpse, Intruder Carcass, or Intruder Egg) into a Hand slot. This Basic pickup has no Noise-roll instruction; taking an Egg still on the Intruder board instead uses the Nest Room Action, costs 2 cards and then rolls Noise.')
s=s.replace('**Intruder Retreat:** during an Injury Effect check,','**Intruder Retreat — move via an Event card:** during an Injury Effect check,')
s=s.replace('**Cockpit** — Check Coordinates (secretly look at the Coordinates card; you may lie; remember it) OR Set Destination (move the Destination marker).','**Cockpit** — Check Coordinates (secretly look at the Coordinates card; you may lie; replace it and remember it) OR Set Destination (move the Destination marker). **The marker selects one of the four destination entries on the Coordinates card:** read the entry corresponding to its track space when checking where the ship will jump.')
s=s.replace('**Hibernatorium** — Try to hibernate (only when the Time marker is on a blue space): Noise roll; if an Intruder shows up (or is present), the attempt fails; otherwise remove your miniature — you are safely hibernating and out of the game until the end.','**Hibernatorium** — Try to hibernate: pay 2 Action cards while present, with Time on a blue space, no Intruder and no Malfunction in the Room. Roll Noise; an Intruder reaching/appearing in the Room makes the attempt fail. Otherwise remove your miniature and stop participating until the end checks. **Once anyone hibernates, no one may change Destination or initiate Self-Destruct as a Character; Coolant Leak Event remains an exception.** A later Hibernatorium Malfunction does not wake/harm sleepers.')
s=s.replace('(2) each Event Phase, each Intruder in a burning Room suffers 1 Injury;','(2) each Event Phase, each Intruder in a burning Room suffers 1 Injury and immediately makes its usual Injury Effect check;')
s=s.replace('The die\'s results (per the rulebook; die faces are symbols): a blank result misses without the Melee miss penalty; a small curled Intruder symbol deals 1 Injury only to a Larva or Creeper (otherwise miss); the larger curved Intruder symbol deals 1 Injury to a Larva, Creeper, or Adult (otherwise miss); a single hit symbol deals 1 Injury to any target; the double-hit symbol deals **2 Injuries when Shooting** to any target before Weapon modifications.','The Combat-die outcomes are listed below; Weapon text can modify Shooting.')
needle='**Intruder Injuries and death:**'
pos=s.index(needle)
table='''| Die result | Shoot | Melee |
|---|---|---|
| Blank | Miss; no Wound penalty | Miss; suffer 1 Serious Wound |
| Small curled Intruder symbol | 1 Injury to Larva/Creeper; miss against other types | Same target restriction and 1 Injury; ineligible target means miss and 1 Serious Wound |
| Larger curved Intruder symbol | 1 Injury to Larva/Creeper/Adult; miss against Breeder/Queen | Same target restriction and 1 Injury; ineligible target means miss and 1 Serious Wound |
| Single hit symbol | 1 Injury to any Intruder type | 1 Injury to any Intruder type |
| Double-hit symbol | **2 Injuries** to any Intruder type before Weapon modifiers | **1 Injury** to any Intruder type |

'''
s=s[:pos]+table+s[pos:]
(R/'repair-09-full-clarity.patch').write_text(''.join(difflib.unified_diff(old.splitlines(True),s.splitlines(True),fromfile='full-iteration-02',tofile='full-repair-01')));p.write_text(s)
