# Audit findings — batch top-001

## dune-imperium-uprising — VERDICT: MAJOR

Source: `extracted/dune-imperium-uprising-rules.txt` (55 KB, read in full).
Prefilter: OK. Source is the genuine Dune: Imperium — Uprising rulebook
(Dire Wolf Digital, © 2023), including the CHOAM Module page, Clarifications,
compatibility section, and the icon guide.

Overall: the base-game rules content is unusually faithful — victory/game-end,
all five phases, agent/reveal turn procedures, combat resolution and ties,
strength values, spies, control/Shield Wall, sandworm rules, acquisition,
trashing, and ~25 spot-checked numbers all match the source. The MAJOR
findings are confined to invented/unsupported CHOAM-module content and a
contradicted component count — exactly the "Contracts/CHOAM" error class this
family-contamination-prone title was flagged for.

### Finding 1 (MAJOR) — Invented mechanic: "Sardaukar Commander" exclusive set-aside contracts

Summary (Leader clarifications): "His **Sardaukar Commander** ability: the two
Sardaukar contracts are set aside as a private pile reserved exclusively for
him (no other player can ever take them) — he does **not** start the game
holding them. He still acquires a Sardaukar contract through the normal
contract-taking mechanism... choosing to take one from his set-aside pile *in
place of* one of the two face-up board contracts."
Repeated in the CHOAM Module section: "With Shaddam Corrino IV in play, two
extra **Sardaukar contracts** are set aside as his exclusive pile; only he can
take them..."

Source: **no support found** (searched: `Sardaukar`, `Commander`, `set aside`,
`aside`, `exclusive`, `reserved`, `contract`). "Sardaukar" occurs only twice:
flavor text "his elite military—the Sardaukar" (line 32) and the board-space
list "Secrets, Sardaukar, and Assembly Hall" (line 344). The source's CHOAM
setup fully accounts for every contract with no set-aside pile: "Shuﬄe the 20
contracts face down, then ﬂip two of them face up... Place the remaining 18
face down in the bank" (lines 856–861), and the module's component list has
only "20 Contract tokens" plus "10 Contract tokens with contrasting backs"
for Rise of Ix (lines 899–906). Two "extra" Sardaukar contracts do not exist
in the source's inventory, and the described setup/acquisition procedure
contradicts the source's 20 = 2 face-up + 18 bank accounting. Players setting
up CHOAM with Shaddam from this summary would perform a setup this rulebook
never describes.

### Finding 2 (MAJOR-supporting) — Unsupported rule presented as canonical, cited to an external FAQ

Summary (CHOAM Module): "If you hold **multiple contracts that name the same
board space**, sending one Agent there completes **all** of them in that
single turn — you gain every matching contract's rewards, resolved in any
order with the board-space and card effects (official FAQ)."

Source: **no support found** (searched: `multiple contract`, `contracts that
name`, `same board space`, `more than one contract`, `complete all`,
`matching contract`). The source's only timing rule is the opposite case:
"If you take a contract involving the board space where you've already sent
your Agent this turn, you must wait until a future turn to complete the
contract" (lines 888–890). The claim is attributed to the official FAQ — i.e.
outside the extracted source — yet sits in a canonical rules section (the
file has no `## FAQ & Rulings` section), so it cannot be verified against the
source at all.

### Finding 3 (MAJOR-supporting) — Contradicted component count: CHOAM contracts

Summary (Components): "CHOAM Module: **20 Contract tokens (10 standard + 10
with different backs for use with Rise of Ix)**"

Source: "20 Contract tokens" AND "10 Contract tokens with contrasting backs"
(lines 899–906); "UPRISING includes 10 **additional** contracts (with
diﬀerent backs)" (line 917); "After setting up the **20 standard contracts**,
shuﬄe the 10 RISE OF IX contracts" (lines 921–924). So: 20 standard + 10
Rise-of-Ix = 30 total, not 20 total with 10 standard. The summary even
contradicts itself — its own CHOAM section correctly says "shuffle 20
Contracts face down" and "after setting up the 20 standard ones."

### Finding 4 (MINOR) — Unsupported "new mechanic" claim: Spice Trade Agent icon

Summary (Overview / Player Reference): "new mechanics: Spies, sandworms, the
**Spice Trade Agent icon**..." / "Key differences from base Dune: Imperium:
... **Spice Trade & Spy Agent icons**"

Source: the differences callout names only one new icon: "There are
additional board spaces requiring 2 Inﬂuence with a Faction, and **a new
Agent icon (Spy)**" (lines 478–480). Spice Trade is listed among the eight
icons (line 476) but never called new. Comparative claim only; does not
change how Uprising itself is played.

### Finding 5 (MINOR) — Unsupported comparative detail: "Arrakis Liaison"

Summary (Player Reference): "Prepare the Way replaces **Arrakis
Liaison**/Foldspace in Reserve"

Source: **no support found** (searched: `Liaison`, `Arrakis Liaison`). The
source's difference note says only "there are no Foldspace cards" (line 262).
The actual Reserve contents (8 Prepare the Way, 10 The Spice Must Flow) are
stated correctly, so play is unaffected.

### Finding 6 (MINOR) — Omission: general Signet Ring / Leader-ability rule

Source: "Each Leader has two diﬀerent unique abilities: The ﬁrst... used
during play as described on the Leader. The second... marked by the Signet
Ring icon, is activated when you play your Signet Ring card on one of your
Agent turns" (lines 292–295; also icon guide lines 1180–1181). The summary
never states this general rule (Signet Ring appears only in the starting-deck
list and in the Shaddam clarification). The icon is printed on the Leader and
card, so tables are unlikely to miss it, but it is a real omission.

### Finding 7 (MINOR) — Omission: collecting accumulated Maker bonus spice

Source (icon guide): "When you send an Agent to one of these board spaces,
you gain all bonus spice there" (lines 1150–1152). The summary describes the
accumulation (Phase 4) but never says how bonus spice is collected. (The
summary defers board-space details to the separate Board Space Guide sheet,
which the source also does in its phase text.)

### Noted, not counted as findings (derivable inferences, per confidence rule)

- Summary's sandworm note ("effects that count 'each sandworm you have in the
  Conflict' include sandworms you summoned earlier the same turn... any
  sandworm in the Conflict is necessarily from the current round") — not in
  source (searched `each sandworm`), but logically entailed by "summon and
  immediately deploy" (lines 556–558), "can never be placed in a garrison"
  (line 558), and "Return any sandworms from the Conﬂict to the bank"
  (line 769).
- "Recalling a Spy 'for no effect'... is the only way to reposition a Spy
  once all three are already on posts" — editorial gloss (searched
  `reposition`); the underlying recall-for-no-effect rule matches lines
  583–585.
- "Combat: Resolved only if units are deployed" — condensation; source gates
  participation on having units (lines 743–744) and gives 0-strength players
  nothing (line 765), but never states the phase is skipped.

### Verification quota

**Victory / game-end / tiebreakers (every sentence):**
- "At the end of a round, if any player has reached 10+ VP or the Conflict
  Deck is empty, the Endgame triggers" ↔ "At the end of a round, if any
  player has reached 10 or more Victory Points (or if the Conﬂict Deck is
  empty), the game ends" (lines 288–290) and "If any player is at 10 or more
  Victory Points on the Score track, or if the Conﬂict Deck is empty, the
  Endgame is triggered" (lines 824–825). MATCH — both directions, no extra or
  missing trigger.
- "First, players may play and resolve any Endgame Intrigue cards. Then the
  most VP wins" ↔ "First, you may play and resolve any Endgame Intrigue cards
  you have. Then whoever has the most Victory Points is declared the winner"
  (lines 842–845). MATCH.
- "Tiebreakers, in order: most spice, then Solari, then water, then
  garrisoned troops" ↔ "tiebreakers are, in order: amount of spice, Solari,
  water, and garrisoned troops" (lines 846–848). MATCH.

**Terms of art:**
- "reach 2 / reach 4 Influence" ↔ lines 329–337 (gain VP at 2, lose below 2;
  bonus at 4 kept; first to 4 takes Alliance token; passed → token and VP
  transfer). MATCH, including the Fenring/Irulan "reach" clarification
  (lines 942–947).
- "Control" ↔ lines 491–508 + 1124–1128 (win titled Conflict → marker on
  flag, replacing opponent's; bonus when ANY player incl. you sends an Agent:
  1 Solari Arrakeen/Spice Refinery, 1 spice Imperial Basin; defensive troop
  from supply when controlled space's Conflict revealed). MATCH.
- "unit in the Conflict" for strength ↔ lines 660–667. MATCH.

**Procedural claims (>5):** Agent turn (one card, one icon, unoccupied space,
costs payable immediately before effects, space + Agent box effects, +1
Faction influence, no-icon cards Reveal-only) ↔ lines 403–448; Reveal turn 3
steps with strength set anytime while resolving (Gurney Halleck note) ↔ lines
646–677, 734–738; Combat Intrigue order/pass/re-enter/consecutive-pass ↔
lines 743–748; reward ladder incl. 3rd-place rules and all three tie cases ↔
lines 750–806; troops to supply not garrison, markers to 0, sandworms to bank
↔ lines 768–769; Makers phase spaces incl. Habbanya Erg (6P) ↔ lines 832–835;
Recall phase ↔ lines 824–829; acquisition (pool/split Persuasion, never
saved, discard pile, refill row of 5) ↔ lines 704–733; Spy place / Infiltrate
/ Gather Intelligence timing / Spy Agent icon no-recall ↔ lines 576–609. All
MATCH.

**Exhaustion rules:** deck empty → reshuffle discard (lines 300–302,
1132–1133; summary's "not usable until reshuffled" consistent, nothing
invented); troops supply empty → can't recruit (lines 535–536, in summary);
contracts exhausted → icon reverts to 2 Solari (lines 873–874, in summary);
bank resources unlimited/substitute (lines 257–260, in summary); Conflict
Deck empty → game end (in summary). MATCH.

NUMBERS_CHECKED: 25, SUPPORTED: 24 (unsupported: CHOAM contract component
breakdown "20 total = 10 standard + 10 Rise-of-Ix" vs source 20 standard + 10
additional = 30; all others match: 10 VP end, conflict deck 1/5/4 of 3/9/4,
5-card hand, 5-card row, strength 2/3/1, +20 flip, deploy +2 from garrison,
influence 2→1 VP / 4→bonus, 2-influence space requirements, score disc 1 in
4P else 0, 3 garrison troops / 12+4 cubes, 1 water, spice 7L/20S, Solari
8L/20S, 20 water, 69/44/18(8+10) cards, 5 objectives, 9 leaders/1–3 icons,
8 sandworms, 3 spies/agents/control markers, 20 contracts → 2 up + 18 bank,
10 RoI contracts → 2 dealt keep 1, control bonuses 1/1, contract icon
2 Solari, doubling example 3→1 VP / 6→2 VP, 8 agent icons.)

VERDICT: MAJOR — the summary embeds an invented Sardaukar-contract subsystem
and an unverifiable FAQ ruling in canonical sections, plus a contradicted
component count; a CHOAM table playing Shaddam from this summary would set up
and take contracts in ways this rulebook never describes.
