# Audit Findings — Zombicide (manual, no ANTHROPIC_API_KEY)

Audited 2026-08-18. `rules/zombicide.md` compared against `extracted/zombicide-rules.txt`
(20-page 1st Edition English rulebook, Guillotine Games/CoolMiniOrNot, 2012/2014 printing).

**Method note**: `ANTHROPIC_API_KEY` was not available in this environment, so
`scripts.verify_summary` (the automated Claude-API fact-check gate) could not run.
This audit was instead performed manually by the same agent that wrote the summary,
following the `.claude/skills/audit-rules/SKILL.md` checklist. Per
`docs/quality/2026-07-03-independent-reaudit.md`, a self-graded check by the
summary's own author is **not equivalent to an independent re-audit** — treat this
verdict as provisional in the same way any freshly-`verified` game is provisional,
and prefer a fresh-agent `/audit-rules` pass (with API access) before relying on it
for the corpus-wide independent-reaudit gate.

Two extraction gaps were found and resolved by rendering the source PDF pages to
images (pymupdf) and reading them directly, per the project's extraction-gap
procedure, rather than guessed:
- The "Noisy Weapons" symbol legend (p.7): confirmed each weapon card marks
  noisiness *per capability* (open-door vs. Melee-kill) independently, with the
  Fire Axe (noisy to open, silent to kill) and Chainsaw (noisy both ways) as the
  book's own worked examples.
- The Car Attack hit threshold (p.17): the extracted text dropped the die-face
  icons ("Each [icon],[icon] or [icon] is a successful hit"); the rendered image
  shows 4-pip, 5-pip, and 6-pip dice, i.e. a hit on 4+.

## Zombicide — PASS

**Verdict: PASS** — the summary is faithful to the source. No invented mechanics,
no contradicted rules, no reversed priority/order, no missing game-end condition.

### Victory / game-end (both directions)

| Summary claim | Source | OK |
|---|---|---|
| Win: all Mission objectives accomplished, immediately, all players win even if Survivors died | "The game is won immediately when all of the Mission objectives have been accomplished... all players win... even if all of a player's Survivors have selflessly given their lives" | Y |
| Loss: all Survivors (all players) killed | "The game is lost when all Survivors have been gruesomely killed and eliminated from the game." | Y |
| No tiebreakers / scoring competition invented | Cooperative game, no scoring/tiebreaker section exists in source | Y (nothing to omit) |

### Numbers checked (18/18 supported)

| # | Claim | Source evidence | OK |
|---|---|---|---|
| 1 | 3 Actions (Blue) / 4 Actions (Yellow+) | "three Actions at the Blue Danger Level. This is increased to four when the Survivor reaches the Yellow Danger Level" | Y |
| 2 | XP thresholds 7 / 19 / 43 for Yellow/Orange/Red | "reaches 7 experience points... Yellow"; "19 experience points, the Orange"; "43 experience points, the Survivor reaches the Red" | Y |
| 3 | Walker/Runner/Fatty = 1 XP, Abomination = 5 XP | "Eliminating a Walker provides 1 experience point"; "Killing a Fatty provides 1 experience point"; "Eliminating a Runner provides 1 experience point"; "Killing an Abomination provides 5 experience points" | Y |
| 4 | Fatty needs 2+ Damage | "You need a 2 Damage weapon to kill them" | Y |
| 5 | Abomination needs 3+ Damage or Molotov | "Only weapons dealing 3 Damage or more can kill this monster. A well-aimed Molotov will do the trick" | Y |
| 6 | Inventory: 5 max, 2 hand slots | "carry up to five pieces of Equipment but can only have two equipped" | Y |
| 7 | Car Attack hits on 4/5/6 | confirmed via rendered page image (p.17) — 4/5/6-pip dice icons | Y |
| 8 | 71 miniatures = 6+40+16+8+1 | component list totals (Survivors/Walkers/Runners/Fatties/Abomination) | Y (arithmetic checked) |
| 9 | 110 mini-cards = 42+62+6 | "110 MINI-CARDS / 42 ZOMBIE CARDS, 62 EQUIPMENT CARDS, 6 WOUNDED CARDS" | Y (arithmetic checked) |
| 10 | Player-count Survivor allotment (4/3/2/1) | Setup step 6, all four bullets | Y |
| 11 | 11 total missions (Tutorial + 10) | TOC: "ten Missions"; body lists Tutorial + 10 named missions | Y |
| 12 | Mission times: Tutorial 20, City Blocks 150, Y-Zone 60, 24hrs Race 90, Drive-by 90, Big W 180, The Escape 150, Grindhouse 45, Zombie Police 180, Might Makes Right 90, Small Town 120 | each mission's own header line (e.g. "TUTORIAL / 4+ SURVIVORS / 20 MINUTES") | Y — all 11 spot-checked individually |
| 13 | frontmatter play_time range 20-180 min | min/max of the above | Y |
| 14 | Might Makes Right = 1-3 players, 1 Survivor each | "designed for one to three players... Each player begins the game with a single Survivor" | Y |
| 15 | Equipment deck reshuffle excludes Wounded/Pans/Molotov/pimpmobile | "reshuffle all the discarded cards, with the exception of Wounded cards, Pans, Molotov, and pimpmobile cards" | Y |
| 16 | Zombie deck reshuffle has no exclusions | "reshuffle all the discarded cards to make a new deck" (no exclusion clause) | Y — confirmed summary does NOT copy the Equipment deck's exclusions onto this one |
| 17 | Yellow Skill is a fixed grant, not a choice (unlike Orange/Red) | image caption: "the Yellow Danger Level, he receives the Extra Skill that's shown here" vs. Orange "pick an extra Skill from the 2 Skills" / Red "pick... from the 3 Skills" | Y |
| 18 | Ranged/Car-attack priority order (Survivors→Walkers→Fatty/Abomination→Runners), filled tier by tier | numbered list "1–Survivors... 2–Walkers... 3–Fatties or Abominations... 4–Runners" + Doug/Sub-MG and Phil/police-car worked examples | Y |

### Procedural claims checked (Turn Structure / Actions)

| # | Claim | Source | OK |
|---|---|---|---|
| 1 | Leaving a Zone with Zombies costs 1 extra Action per Zombie | "he must spend one extra Action per Zombie to leave the Zone" | Y |
| 2 | Search: indoors only, no Zombies in Zone, 1/turn even if free | "You can only Search Zones inside a building and only if there are no Zombies... A Survivor can only perform a single Search Action per turn, even if it's an extra, free Action" | Y |
| 3 | Opening a building's door for the first time spawns Zombies in every connected Zone via one card draw per Zone | "Opening a building for the first time reveals all the Zombies inside all rooms... draw a Zombie card for each Zone" | Y |
| 4 | Reorganize/Trade costs 1 Action; trade partner reorganizes free; discarding-to-make-room is separately free/anytime | "At the cost of one Action, a Survivor can reorganize... simultaneously exchange... This other Survivor may reorganize his own inventory for free" + "You may discard cards from your inventory to make room for new cards at any time, for free" | Y |
| 5 | Driving is not a Move Action, ignores Move modifiers/penalties | "This Action is not a Move and is not subject to movement modifiers... nor is it affected by disadvantages related to Move Actions" | Y |

### Term-of-art definitions

| Term | Summary | Source definition | OK |
|---|---|---|---|
| Actor | Survivor or Zombie | "ACTOR: A Survivor or Zombie." | Y |
| Zone | room indoors / street segment between crossings, can span 2-4 tiles | "Inside a building, a Zone is a room. On the street, a Zone is the area between two pedestrian crossings... may extend over two tiles or even four tiles." | Y |
| Line of Sight (building) | 1 Zone max, only through a shared opening, closed door blocks | "sees into all Zones that share an opening... limited to the distance of one Zone" | Y |

### Exhaustion rules

| Claim | Source | OK |
|---|---|---|
| Equipment deck reshuffled minus Wounded/Pans/Molotov/pimpmobile | quoted above (#15) | Y |
| Zombie deck reshuffled with no exclusions | quoted above (#16) | Y |
| No invented reshuffle/replenish rule beyond these two | scanned full text for "empty/run out/exhaust/reshuffle" — only these two cases exist | Y |

### Mechanics / invented-content check

Scanned every Action, every Zombie-Phase step, every Skill category named in the
summary against the source; none are invented. The "Skills" bullet in Special
Rules & Edge Cases is explicitly scoped as "Representative Skills" (the source
lists ~30; the summary names 9 as examples) — this is a disclosed scope
limitation, not a fabricated or contradicted mechanic, so it is not counted as a
finding.

### Player Reference tables

All four tables (Turn Order, Danger Level/XP, Experience per Kill, Hit-Assignment
Priority, Inventory Limits) cross-checked row-by-row against the numbers above —
no scrambling found.

**NUMBERS_CHECKED: 18, SUPPORTED: 18**
