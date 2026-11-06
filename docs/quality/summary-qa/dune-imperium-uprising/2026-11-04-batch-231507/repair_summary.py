from pathlib import Path
import hashlib,json
q=Path(__file__).resolve().parent;p=Path('/home/jonny/projects/boardgame-rules/rules/dune-imperium-uprising.md')
s=p.read_text();assert hashlib.sha256(p.read_bytes()).hexdigest()==json.loads((q/'input-manifest.json').read_text())['files'][0]['sha256'],'Unexpected canonical modification; preserve before overwrite'
s=s.replace('player_count: "1-6"','player_count: "2-4"')
a=s.index('Games for one or two players require');b=s.index('\n\n## Components',a)
s=s[:a]+'''**Scope:** Original English 2023 Uprising, rulebook version 23-10-12: complete standard 2–4-player play, including the required two-player Rival rules below, plus the optional standard base-box CHOAM Module. Solo-only rules, all optional Rival variants (including Streamlined Rivals), six-player teams and cross-game expansions are excluded. In two-player play use an ordinary scoring Rival, rather than the two Streamlined-only Rivals Lady Amber Metulli and Glossu “The Beast” Rabban. The 10 contrasting-back Rise of Ix contracts are identified for sorting only and are not used in this scope. Board-space rules come from the publisher’s Uprising Board Space Guide; the labeled FAQ section uses relevant clarifications from the official January 13, 2025 FAQ.''' +s[b:]
s=s.replace('(in a six-player game, also Habbanya Erg)','').replace('(or six) ','').replace('four (or six)','four')
s=s.replace('(the Rise of Ix expansion adds a third, dreadnoughts)','')
a=s.index('**CHOAM with Rise of Ix:**');b=s.index('## Player Reference',a)
s=s[:a]+'''The **10 contrasting-back contracts** are a separate Rise of Ix compatibility set; leave them in the box for standard CHOAM. They do not reduce the 20 standard contracts to 10.

## Board Space Guide — Standard 2–4 Players

The listed Agent icon is required unless the Spy Agent icon permits access. Pay entry costs and meet Influence requirements before effects. “Combat” permits normal deployment; spaces not marked Combat do not. Only a Faction’s actual board spaces automatically give its Influence: Imperial Privilege, Shipping and Sietch Tabr are not Faction-icon spaces.

| Space (Agent icon) | Cost / requirement | Effects |
|---|---|---|
| Accept Contract (Spice Trade) | None | Draw a card; take a contract with CHOAM, otherwise gain 2 Solari (also if no contracts remain). |
| Arrakeen (City), Combat | None | Recruit one troop and draw one card; controller gains 1 Solari. |
| Assembly Hall (Landsraad) | None | Draw an Intrigue; gain 1 Persuasion during your Reveal turn if your Agent is here. |
| Deep Desert (Spice Trade), Combat | 3 water | Gain all bonus spice; choose either 4 base spice OR, with Maker Hooks, summon two sandworms. |
| Deliver Supplies (Spacing Guild) | None | Gain 1 Guild Influence and 1 water. |
| Desert Tactics (Fremen), Combat | 1 water | Gain 1 Fremen Influence, recruit one troop, and optionally trash a card. |
| Dutiful Service (Emperor) | None | Gain 1 Emperor Influence; take a contract with CHOAM, otherwise 2 Solari (also if none remain). |
| Espionage (Bene Gesserit) | 1 spice | Gain 1 Bene Gesserit Influence, draw a card, place a Spy. |
| Fremkit (Fremen), Combat | None | Gain 1 Fremen Influence and draw a card. |
| Gather Support (Landsraad) | Choose 0 or 2 Solari | Recruit two troops; if 2 Solari paid, also gain 1 water. |
| Hagga Basin (Spice Trade), Combat | 1 water | Gain all bonus spice; choose either 2 base spice OR, with Maker Hooks, summon one sandworm. |
| Heighliner (Spacing Guild), Combat | 5 spice | Gain 1 Guild Influence and recruit five troops. |
| High Council (Landsraad) | 5 Solari each visit | First visit: put Councilor on unoccupied seat; gain 2 Persuasion on every Reveal turn for rest of game. Subsequent visits: gain 2 spice, draw an Intrigue and recruit three troops. |
| Imperial Basin (Spice Trade), Combat | None | Gain 1 base spice plus all bonus spice; controller gains 1 spice. |
| Imperial Privilege (Landsraad) | 3 Solari; 2+ Emperor Influence | May discard an Intrigue to draw an Intrigue. Recall one of your other Agents and draw a card. |
| Research Station (City), Combat | 2 water | Recruit two troops and draw two cards. |
| Sardaukar (Emperor) | 4 spice | Gain 1 Emperor Influence, draw an Intrigue and recruit four troops. |
| Secrets (Bene Gesserit) | None | Gain 1 Bene Gesserit Influence and draw an Intrigue. Each opponent with 4+ Intrigues gives you one selected at random. |
| Shipping (Spice Trade) | 3 spice; 2+ Guild Influence | Gain 5 Solari and 1 Influence with any one Faction. |
| Sietch Tabr (City), Combat | 2+ Fremen Influence | Choose: take Maker Hooks if you lack them, recruit one troop and gain 1 water; OR gain 1 water and optionally remove Shield Wall. |
| Spice Refinery (City), Combat | Choose 0 or 1 spice | Gain 2 Solari, or 4 Solari if you paid 1 spice; controller gains 1 Solari. |
| Swordmaster (Landsraad) | 8 Solari before anyone gains Swordmaster; 6 once anyone has one | Only once per player per game. Take third Agent from beside board onto Leader; available this round and for rest of game. A Rival gaining its Swordmaster also reduces the human cost to 6. |

## Required Rival Rules — Standard Two-Player Game

Use **one shared scoring Rival** as the third competitor. It can win: its 10+ VP triggers Endgame at Recall just like a human’s score. Select its Rival card; follow its printed Signet Ring and Scheme abilities and its left-to-right Faction priority list. Its printed Swordmaster value sets its resource threshold; lower values are more challenging. Do not apply solo difficulty adjustments or optional Rival variants.

**Setup:** Give it a color, four cubes at the bottom of Influence tracks, three troops in its garrison and the remaining troops in supply, two Agents in supply and Swordmaster beside the board, three Spies and 1 water in supply. Its score and Combat marker start at 0. Shuffle House Hagal, retaining the 2P Reshuffle card. Give the Rival the Ornithopter Objective; randomly deal the other two eligible Objectives to the humans, with First Player going to the human whose card shows it. First Player alternates only between humans. Each round the Rival is considered immediately clockwise from First Player, so turn order is First Player → Rival → other human. Restore its Agents to its supply at Recall for the next round.

**Agent turns:** A Rival takes Agent turns while an Agent remains in supply and never takes a Reveal turn. Reveal House Hagal cards until an Agent can be placed on an unoccupied indicated space. Ignore an occupied destination and reveal again. With a two-destination card, select only the destination matching the current conditions (Guild Influence for Accept Contract/Shipping; Conflict tier for Deliver Supplies/Heighliner); if that destination is occupied, reveal a new card, without using the other destination. If House Hagal empties or Reshuffle appears, immediately reshuffle it and continue.

Ignore normal space costs and effects: apply only the revealed House Hagal effects, including printed resource gains, Influence, Signet Ring, troop, Spy and Maker Hooks icons. A numbered Influence icon refers to that position in the Rival card’s Faction priority list. Some cards provide a bonus at 2+ Influence; lack of that bonus never prevents placing the Agent. For example, its Gather Support card recruits one troop and, with 2+ Emperor Influence, also gains one Influence with its second-priority Faction. For troop icons, recruit from supply; at a Combat space deploy all newly recruited troops, otherwise put them in garrison. At every Combat space also deploy up to two available troops from garrison, even when the card recruited none. Stolen Intrigues come randomly from each opponent with 4+ Intrigues. Rivals use Intrigues as resources, rather than playing their text.

**Spies and Schemes:** Unless a post type is specified, place a Spy at the first available Faction observation post in priority order; if all four are occupied ignore placement. A Place Spy card uses an empty post of its specified type, or ignores placement if none exists; either way reveal another Hagal card because it has not sent an Agent. Rivals never recall Spies to Infiltrate or Gather Intelligence. Placing their third and final supply Spy immediately recalls their other two Spies and triggers their printed Scheme. If a Scheme recruits troops before Agent placement and the Rival then visits a Combat space that same turn, deploy those troops too.

**Resources and Swordmaster:** Collect resources from Hagal effects and Conflict rewards, not ordinary space effects or 4-Influence track bonuses (the Maker and control exceptions below still apply). Count Solari, spice, Intrigue cards and water together, each unit counting as one. As soon as this total reaches the Rival’s printed Swordmaster value, spend that many resources and take its third Agent, usable in the current round. If choosing which resources to spend, use Solari first, then spice, then Intrigue cards, then water; keep leftovers. After obtaining Swordmaster, whenever it has **7 Solari**, **7 spice**, **3 Intrigue cards**, or **3 water**, spend each such set for 1 VP. The Rival gains and loses Influence VP and Alliances like a human, but does not receive the resource bonus for reaching 4 Influence.

**Maker spaces:** The Rival always collects all bonus spice at a visited Maker space. At Hagga Basin or Deep Desert, with Maker Hooks and a Conflict that permits sandworms, summon one or two sandworms respectively instead of taking base spice. If it summons none, take the space’s base spice instead (Hagga 2, Deep Desert 4; Imperial Basin always 1). A Hagal Maker Hooks icon takes a token if needed. A Hagal Shield Wall removal effect removes the wall only if the Rival has Maker Hooks; otherwise ignore it.

**Combat:** At the beginning of Combat, if the Rival has at least one unit deployed, reveal one Hagal card in turn order. Ignore everything except its bottom swords, adding that many strength; on Reshuffle, reshuffle and reveal again. Humans then have their normal Combat Intrigue window. The Rival receives normal placement rewards, doubles rewards with one or more sandworms, and wins Conflict cards and battle-icon VP normally. It gains control bonuses when any human or Rival visits its controlled space and the defensive troop from supply when that Conflict is revealed. When choosing Influence, use the Faction with least Influence, breaking ties by leftmost priority icon. Always take an optional Conflict VP if it can pay the resources or recall the required Spies. It **never takes contracts**: a contract reward gives it 2 Solari, even with CHOAM. Combat cleanup and two-/three-player reward and tie rules apply normally.

## FAQ & Rulings

These are relevant base-game clarifications from Dire Wolf’s **official FAQ, January 13, 2025**, pp1–4; they supplement the original rulebook rather than importing expansion rules.

- **Mandatory effects and costs:** Most card and space effects are mandatory. Exceptions include “may,” arrow costs you can decline, and the optional black-X trash icon. A direct instruction to trash a card itself is mandatory. Intrigue conditions and costs must be met to play that Intrigue. Optional arrow effects can only be paid once, except doubled Conflict rewards.
- **Alliance loss:** If the holder loses Influence after being tied, the formerly tied player takes the Alliance; if several were tied, the former holder chooses which receives it. Falling to 3 or lower also loses the Alliance; if nobody has 4+ to take it, return it to the board. Losing the Alliance loses its VP.
- **Contract completion is mandatory:** Fulfill all contracts you hold for the same space with one Agent placement. A board-space contract is another effect of that Agent turn and can resolve in any order with space and Agent-box effects. This does not waive the rule that you must hold it when sending the Agent.
- **Shaddam:** Sardaukar Commander permits choosing a set-aside Sardaukar contract instead of a generally available one when acquiring a contract; these contracts do not start in your possession. Emperor of the Known Universe takes effect immediately on playing Signet Ring to send an Agent, but lasts only for that turn, not the round. Follow the printed Leader for its deployment restriction.
- **Spies:** Recalling a Spy still requires playing a card for the Agent turn and does not waive costs or requirements. You may recall two Spies for different effects (one Infiltrate, one Gather Intelligence), never two to Gather Intelligence on the same placement. Maker Hooks are retained, not spent, when summoning.
- **Draw timing:** Drawn during Reveal means immediately reveal and use that card this turn. Drawn after Reveal means keep it for next round, then draw five additional cards. A Plot Intrigue with a later Reveal effect stays face up until then, is used, then discarded. If the Intrigue deck runs out, shuffle its discard to form a new deck.
- **Combat and troops:** All troops newly recruited that turn, including from an Intrigue, can deploy at a Combat space; old garrison troops cannot be re-recruited to bypass the two-troop limit. “When you win a Conflict” Intrigues cannot be played after tying for first; if received as a winning reward they can be played immediately. Chani’s Leader treats troops returned to supply at Combat resolution as lost, handling different sources of retreat/loss separately. “Retreat any number” allows zero.
- **Victory:** The Spice Must Flow’s acquire VP is retained if the card is later trashed. Scores may exceed the printed track’s 12. If all four resource tiebreakers remain tied, the player who most recently took a Reveal turn wins.
- **Reverend Mother Jessica** may use her ability on the turn she flips. **False Orders:** affected opponents move their Spy to an empty post not connected to your Agent’s destination that turn; it may be played even if no enemy Spy is connected there. **Manipulate:** opponents cannot acquire the removed card; you may acquire it by other means without the 1-Persuasion discount; if unacquired by the end of your next Reveal, remove it from game. **Litany Against Fear:** ignore its red box during Reveal, or when it gains an Agent icon and is played normally as an Agent card.

''' +s[b:]
p.write_text(s)
(q/'repair-01-notes.md').write_text('Repaired scope, complete board guide, required standard two-player Rival procedures and relevant official FAQ clarifications. Preserved historical verification status pending independent audit and coordinator stamp. The old banner alleges some CHOAM claims lack support; the recovered official FAQ now directly supplies those rulings (FAQ p1 contract, p3 Shaddam). This is source recovery, not invented mechanics.\n')
