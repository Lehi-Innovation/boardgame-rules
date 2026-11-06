# Identity corrections and source findings

The user chose to identify games by their **name and description**, correcting clearly wrong BGG IDs. The original 831 named targets remain in the inventory. Original IDs and supporting primary BGG metadata are retained in `identity-corrections.json` and `corrected-identity-evidence.json`.

Twenty-eight numeric ID corrections and one withdrawn wrong association are recorded. A withdrawn association remains explicitly unresolved until a replacement ID is confirmed; the named target is retained.

| Named game | Original BGG ID | Corrected BGG ID |
|---|---:|---:|
| Beat the Buzzard | 699 | 175 |
| Carla Caramel | 328614 | 351937 |
| Summoner Wars (Second Edition) | 58281 | 332800 |
| Medina | 1261 | 167270 |
| Santorini | 9963 | 194655 |
| FITS | 10565 | 40393 |
| Domination | 16620 | 789 |
| Samsara | 154274 | 246746 |
| Blockade | 2710 | 2559 |
| Castle Risk | 3834 | 2557 |
| Saga | 2214 | 101865 |
| Alcazar | 45319 | 992 |
| Artifact | 4271 | 144310 |
| Breakout: Normandy | 20203 | 730 |
| Citadel of Blood | 4117 | 3248 |
| Bloody Ridge | 11964 | 8746 |
| Cobra: Game of the Normandy Breakout | 4092 | 4008 |
| Dirtside II | 2591 | 5687 |
| Don't Drop the Soap | 32687 | 236360 |
| Game of the Generals | 2728 | 315883 |
| Granada: The Fall of Moslem Spain | 58099 | 5453 |
| Mall Madness | 15162 | 5086 |
| Thunder Road: Vendetta | 804 | 342070 |
| Apocalypse | 2574 | 14123 |
| Cardino | 2405 | 2116 |
| Battle of the Bulge | 16444 | 4252 |
| Gridlock | 22428 | 35205 |
| Pole Position (Parker Brothers, 1983) | 7993 | 2732 |
| 3-6-9 (Alex Raulli card game) | 32597 | Unresolved; wrong association withdrawn |

## Superseded identity findings

Earlier Domination and Samsara MAJOR findings treated the stored IDs as authoritative. Those findings are withdrawn under the user’s explicit policy; their history is preserved in `superseded-identity-findings.yaml`. They do not establish gameplay errors in the intended games.

Domination describes Sid Sackson’s Focus, also sold as Domination. A complete German Kosmos 1995 Focus manual is now accepted. The unrelated Patch Products domino source is preserved under `rejected/`, with its original hashes in the inventory.

Samsara describes the Oka Luda deckbuilder, rather than Thomas Weber’s marble-track game. Its ID/designer metadata is corrected. The archive’s English and French PDFs were beta drafts and remain rejected. A final English retail rulebook is now accepted from the publisher’s current rules/download page: ten PDF spreads, twenty printed pages, with no draft/beta label.

## Source-backed summary errors

Kitty Bitty’s Blue Orange 2018 foldout lists **nine Mommy Cats**, but the summary lists four. A caught kitten **does not move forward**; the summary instead says it goes back and introduces an unspecified variant. These specific MAJOR findings are recorded in the semantic audit tracker. They are not a complete audit of the summary.

Schotten Totten’s old MAJOR verdict only said that source text was missing. That availability-only verdict is archived in `superseded-availability-findings.yaml`; candidate recovery alone does not establish accuracy or earn a PASS.

Blockade’s corrected primary record (BGG 2559) and matching rules require **one pawn** to reach either opponent home space. The summary instead requires both pawns to reach the opponent corner. That specific MAJOR finding is retained; it is not a full audit.

## Title collisions

The legacy archive also contains unrelated Black Box, Blockade, Giganten, Saga, Gambler and Razzia manuals. Those downloads are rejected with reasons in the inventory. Blockade and Saga now have corrected identities and accepted matching sources. The unrelated legacy manuals remain rejected. Never accept a matching title without inspecting the game itself.

Alcazar’s description identifies Martin Davison’s 1978 two-pawn/eight-wall game (BGG 992), not Wolfgang Kramer’s 2009 castle-building game. Artifact’s description identifies the 2013 museum game (BGG 144310), not the 1980 lunar-combat game. Both now have correct IDs and sources. Apocalypse is now resolved as Elliott’s simultaneous-move chess variant, with a matching source. Battle of the Bulge is now resolved as the specifically described SPI/Dunnigan 1979 Bulge (BGG 4252), with its original SPI rulebook. The separate Avalon Hill 1965 identity (16444) remains preserved as the original wrong ID.

## Further named-game corrections — 2026-11-05

- Cobra: Game of the Normandy Breakout: 4092 → 4008. Named SPI Normandy breakout game, not wordXchange.
- Dirtside II: 2591 → 5687. Named Ground Zero Games science-fiction miniature rules, not Carcassonne: The River.
- Don't Drop the Soap: 32687 → 236360. Description is 59-card hot-potato game by Pedersen, not 2007 Sebelius six-location board game.
- Game of the Generals: 2728 → 315883. Named Philippine Salpakan with human arbiter, not electronic 1980 The Generals reimplementation.

Primary public BGG API records were checked; corrected identity evidence is preserved in `corrected-identity-evidence.json`. Correcting an ID does not establish summary accuracy or accept a mismatched rulebook.

- **Granada: The Fall of Moslem Spain**: BGG 58099 → [5453](https://boardgamegeek.com/boardgame/5453/granada-the-fall-of-moslem-spain). Named 2003 Robert Markham/Avalanche Press Reconquista wargame, not the 2009 Queen Games city-building Granada. Primary API record checked; summary accuracy remains unaudited.

- **Mall Madness**: BGG 15162 → [5086](https://boardgamegeek.com/boardgame/5086/electronic-mall-madness). Description is the full-size talking electronic 3D shopping-mall game, not the cassette-sized Flipsiders Mall Madness. Primary API record checked; summary accuracy remains unaudited.

- **Thunder Road: Vendetta**: BGG 804 → [342070](https://boardgamegeek.com/boardgame/342070/thunder-road-vendetta). Named Restoration Games 2023 Vendetta, with hazards, damage tokens and command board, not the original 1986 Milton Bradley Thunder Road. Primary API record checked; summary accuracy remains unaudited.

- **Apocalypse**: BGG 2574 → [14123](https://boardgamegeek.com/boardgame/14123/apocalypse). Named 1976 C. S. Elliott simultaneous-move chess variant with two knights and five pawns per side, not Classic Warlord or Games Workshop nuclear-war Apocalypse. Primary API record checked; summary accuracy remains unaudited.

## Additional source-backed summary errors — 2026-11-05

DeathStacks omits the inventor’s partial-stack moves and mandatory reduction of stacks taller than four. Fields of Action incorrectly prohibits jumping/isolated-piece moves, requires ascending capture order and allows passing when immobile. Specific MAJOR findings are recorded in [the source-recovery findings](../audit-findings/source-recovery-2026-11-05.md); these are not full summary audits.

Pentominoes also has a specific MAJOR finding: its competitive rules use a shared unused-piece pool and last-legal-placement victory; the summary divides pieces and uses passing/piece-count scoring. The university reference and Golomb’s column independently support the correction. This is not a full audit.

- **Cardino**: BGG 2405 → [2116](https://boardgamegeek.com/boardgame/2116/cartino). Named Cardino matches Cartino, the 1969 playing-card-suit tile-placement game; Cardino is an explicit primary BGG alternate name. Correct identity is 2116, not stored Bezique 2405, a traditional trick-taking card game. The archive links a matching original Ravensburger Cartino rulebook. Summary publisher and gameplay details remain unaudited. Primary API record checked; summary accuracy remains unaudited.

- **Battle of the Bulge**: BGG 16444 → [4252](https://boardgamegeek.com/boardgame/4252/the-big-red-one-the-game-of-the-first-infantry-div). Named summary explicitly describes Jim Dunnigan/SPI 1979 divisional Bulge, with daily turns, 8-km hexes, two combat tables, weather/air power and bridge-interdicted supply. Primary 4252 lists Bulge: The Battle for the Ardennes as an alternate and describes that same supply/victory system. Original SPI 1979 manual title and contents visually match. Stored 16444 is the separate Avalon Hill 1965 game by Pinsky/Shaw. Preserve the original named target and correct its ID to 4252; no claim of summary accuracy. Primary API record checked; summary accuracy remains unaudited.

- **Gridlock**: BGG 22428 → [35205](https://boardgamegeek.com/boardgame/35205/gridlock). Named description is Andrew Looneys 1997 Icehouse-pyramid chessboard game with placement/drop phases and directional turning. Primary BGG 35205 identifies that exact game and designer and links the same Wunderland creator rules. Stored 22428 is now an administrative Outside the Scope of BGG catch-all, not this game. Preserve original ID and named target; correct to 35205. No full summary accuracy claim. Primary API record checked; summary accuracy remains unaudited.

- **3-6-9**: incorrect BGG 32597 withdrawn; replacement ID unresolved. The named description exactly matches [Alex Raullis Pagat card game](https://www.pagat.com/invented/369.html), including negative trick thresholds and card-removal variants. The former ID identifies Paul Townsends unrelated abstract game. Original IDs remain preserved; source recovery does not invent a BGG association.

- **Pole Position**: BGG 7993 → [2732](https://boardgamegeek.com/boardgame/2732/pole-position). Named summary explicitly identifies Parker Brothers and a 2–4-player first-car racing game. Primary BGG 2732 is the 1983 Parker Brothers arcade adaptation with movement cards and one car per player. Stored 7993 identifies Gerhard Kodys 1989 Piatnik game with three cars per player, simultaneous numbered-card selection and combined placement scoring. Preserve the original named target and ID history; correct the association to 2732. Detailed summary dice/speed/lap claims remain unaudited. Primary API record checked; summary accuracy remains unaudited.

- **Gespensterburg**: BGG 229553 → [103192](https://boardgamegeek.com/boardgame/103192/gespensterburg). Named Noris game and description explicitly match the 1994 Johann/Michael Rüttinger trivia, rhyme, tongue-twister race to the Black Raven, BGG103192. Original229553is the unrelated1990REMUS cassette/spinner game. Correct ID under user instruction; preserve original and earlier wrong-target research as history. Source discovery does not certify the generated summary. Primary API record checked; summary accuracy remains unaudited.
