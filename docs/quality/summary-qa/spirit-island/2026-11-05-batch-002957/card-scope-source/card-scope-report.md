# Spirit Island original base-game card scope verification

Capture/verification date: 2026-11-05 UTC. Scope: original 2017 base game; no expansion cards. No questions, answer keys, reader results, grades, or other reviewer reports were consulted. The canonical summary was inspected only to identify names. This is a source-scope investigation, not the final source audit.

## Finding

**Two named cards are outside scope: Sky Stretches to Shore (Branch & Claw Minor) and Cast Down into the Briny Deep (Branch & Claw Major).** All other 29 named Power/Fear card identities located in the summary are base-game cards. The fact that a cross-card ruling appears under the Core FAQ filter is not membership evidence and was not used as such.

Original printed faces of the two expansion cards each show the same small white triskelion at bottom right. The publisher-linked Branch & Claw rulebook, printed/PDF page 6, explicitly identifies this corner mark as the expansion-material identifier for removing expansion materials when playing core only. The rendered page preserves the actual symbol, which text extraction omits. The other 29 original-layout faces have no expansion mark; their core classification is corroborated by catalog locators, with independent explicit designer core-printing evidence for eight titles as noted below. Catalog set labels alone are not treated as primary proof.

## Primary source chain and raw artifacts

- Publisher page: https://shop.greaterthangames.com/products/spirit-island-branch-claw — `publisher-branch-claw.html` preserves its “Download here” link.
- Publisher-linked PDF URL: https://www.dropbox.com/scl/fi/92e90f2pvo77yrgkrlfly/SI_B-C_Rulebook.pdf?rlkey=v577gnumjvj756sxeiu294mm1&st=qj5bpd66&dl=0 . Captured PDF: `branch-claw-rulebook.pdf`. Identical PDF bytes were also captured as `branch-claw-dropbox-content.pdf` using https://dl.dropboxusercontent.com/scl/fi/92e90f2pvo77yrgkrlfly/SI_B-C_Rulebook.pdf?rlkey=v577gnumjvj756sxeiu294mm1 . Both SHA256 values are in `provenance.jsonl`.
- Primary legend: `branch-claw-rulebook-p6.png` renders the complete printed/PDF page 6 from that PDF; `branch-claw-rulebook.txt` is its text extraction.
- Designer FAQ: https://querki.net/raw/darker/spirit-island-faq/Changes-in-core-game-second-printing — `core-second-printing.html` and derived `core-second-printing.txt`. Explicitly names Dahan Enheartened, Dahan Raid, Blazing Renewal, Entwined Power, Poisoned Land, Powerstorm, Tsunami, and Dread Apparitions in core printing changes. This positively identifies these core cards rather than relying on the broad Core tag.
- Original printed card-face images are preserved as the `.jpg` files listed below. Their hosts are community catalogs, but the printed publisher material itself (card title and visible presence/absence of the expansion identifier), cross-checked with the official legend, is the evidence. Full individual public source URLs, UTC capture timestamps, byte counts, and SHA256 values are preserved in `provenance.jsonl`. Power URLs follow `https://sick.oberien.de/imgs/powers/FILENAME`; Fear URLs follow `https://sick.oberien.de/imgs/fears/FILENAME`.
- `catalog-cards.js` from https://sick.oberien.de/cards.js was used only to locate all named cards and images, and triage set claims. `all-named-card-title-corner-strips.jpg` is a derived inspection aid showing all 31 titles and their complete bottom-corner regions; full original images remain available.

## Eight prioritized cards

| Card | Set/type | Primary proof | Uncertainty |
|---|---|---|---|
| Sky Stretches to Shore | Branch & Claw / Minor | `sky_stretches_to_shore.jpg`: triskelion lower right, matched to official B&C p.6 legend | None material for exclusion |
| Cast Down into the Briny Deep | Branch & Claw / Major | `cast_down_into_the_briny_deep.jpg`: triskelion lower right, matched to official B&C p.6 legend | None material for exclusion |
| Blazing Renewal | Original core / Major | `blazing_renewal.jpg`: no expansion mark; explicitly named under Major changes in designer core second-printing page | No membership uncertainty; face preserves first-printing threshold wording |
| The Trees and Stones Speak of War | Original core / Major | `the_trees_and_stones_speak_of_war.jpg`: original face, no expansion mark | Community-hosted scan; no independent publisher inventory hash |
| Encompassing Ward | Original core / Minor | `encompassing_ward.jpg`: original face, no expansion mark | Same scan limitation |
| Dahan on their Guard | Original core / Fear | `dahan_on_their_guard.jpg`: original face, no expansion mark | Same scan limitation |
| Wrap in Wings of Sunlight | Original core / Major | `wrap_in_wings_of_sunlight.jpg`: original face, no expansion mark | Same scan limitation |
| Infinite Vitality | Original core / Major | `infinite_vitality.jpg`: original face, no expansion mark | Same scan limitation |

## All additional named Power/Fear identities

All entries below are original core; every listed original-layout face was inspected for expansion marks. None has one. “Explicit core printing list” is additional independent primary evidence where present.

| Card | Type | Original face file | Additional primary corroboration |
|---|---|---|---|
| Harbingers of the Lightning | Unique | `harbingers_of_the_lightning.jpg` | — |
| Boon of Vigor | Unique | `boon_of_vigor.jpg` | — |
| Mantle of Dread | Unique | `mantle_of_dread.jpg` | — |
| Crops Wither and Fade | Unique | `crops_wither_and_fade.jpg` | — |
| Words of Warning | Unique | `words_of_warning.jpg` | — |
| Tidal Boon | Unique | `tidal_boon.jpg` | — |
| Dread Apparitions | Unique | `dread_apparitions.jpg` | Explicit core printing list |
| Call on Midnight's Dream | Unique | `call_on_midnights_dream.jpg` | — |
| Song of Sanctity | Minor | `song_of_sanctity.jpg` | — |
| Veil the Night's Hunt | Minor | `veil_the_nights_hunt.jpg` | — |
| Poisoned Land | Major | `poisoned_land.jpg` | Explicit core printing list |
| Entwined Power | Major | `entwined_power.jpg` | Explicit core printing list |
| Powerstorm | Major | `powerstorm.jpg` | Explicit core printing list |
| Tsunami | Major | `tsunami.jpg` | Explicit core printing list |
| Vengeance of the Dead | Major | `vengeance_of_the_dead.jpg` | — |
| Indomitable Claim | Major | `indomitable_claim.jpg` | — |
| Mists of Oblivion | Major | `mists_of_oblivion.jpg` | — |
| Dissolve the Bonds of Kinship | Major | `dissolve_the_bonds_of_kinship.jpg` | — |
| Scapegoats | Fear | `scapegoats.jpg` | — |
| Dahan Raid | Fear | `dahan_raid.jpg` | Explicit core printing list |
| Dahan Enheartened | Fear | `dahan_enheartened.jpg` | Explicit core printing list |
| Overseas Trade Seem Safer | Fear | `overseas_trade_seem_safer.jpg` | — |
| Trade Suffers | Fear | `trade_suffers.jpg` | — |

The summary's “Call on Midnight's Dreams” is the card printed **Call on Midnight's Dream** (singular). Its “Overseas Trade Seems Safer” corresponds to the original face printed **Overseas Trade Seem Safer**. These are identity/title observations, not additional expansion findings. Generic “unrest” in prose was not counted as the Branch & Claw Fear card **Unrest**. Gift of Strength, Shadows of the Dahan, and the other named panel abilities are not separately acquired Power/Fear cards; they were not misclassified as deck cards.

## Bounded reading and checks

- Authoritative B&C legend: complete extracted PDF p.6, text character offsets [4798,6407), 1609 characters, printed with no truncation; complete page rendered and visually inspected. The omitted symbol in text was explicitly resolved visually.
- Designer printing page: derived text has 7237 characters. Relevant beginning [0,1400), plus Major/Unique region [1491,2791) and [1510,2810) read in bounded outputs; relevant sections complete. The remainder concerns rulebook/punchboard changes and was not needed for card membership.
- Publisher page: link extraction prints the exact one Dropbox anchor without dumping full HTML.
- Catalog locator: relevant matching constructor lines and image-path methods inspected in bounded outputs; full 275958-byte script preserved, not claimed read exhaustively.
- Full eight prioritized faces were viewed individually. All 31 original title/corner regions were visually inspected in the derived contact sheet. No source-content read relied on an ellipsis-truncated output; initial search snippets were discovery aids only.
- SHA256 provenance checks and extraction/render hashes are recorded in `provenance.jsonl`. Original downloads are preserved unmodified. Third-party image hosting limits provenance to the retrieved original printed face rather than an authenticated publisher card archive; the positive expansion-symbol comparison is strong and direct, and no additional suspected expansion cards remain.

## Scope corrections for parent

Remove the Sky Stretches to Shore-specific teaching/example and the Cast Down into the Briny Deep board-destruction example from a base-game-only summary. The general core rules may remain if independently supported. Keep the other six prioritized cards and all 23 additional core identities. Any question-bank or final-testing scope correction belongs to the parent workflow; no summary or bank edits were made here.
