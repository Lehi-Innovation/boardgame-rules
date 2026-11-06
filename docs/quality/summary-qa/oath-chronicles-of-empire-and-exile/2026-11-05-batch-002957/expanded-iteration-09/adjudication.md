# Iteration 09 independent adjudication

Assessed all 104 fixed questions for each reader (208 entries, 656 required fact-group assessments) against expanded-v11 and the frozen effective scope-v12. The complete packet and snapshot were delivered first in contiguous marked chunks of at most 5,000 Unicode characters, at most two chunks per call, with inner and outer output budgets of at least 7,000 tokens. No previous grades, audits, other candidates or source documents were used.

Every original entry was reconstructed from its own Unicode half-open spans. Object/string types, metadata, original text/verbatim fields, answer joins and all numeric fields were preserved; all 208 reconstructed entries equal their actual raw originals. The six manifest input hashes were recomputed from actual bytes and matched. Fixed questions, answer-key strings, required fact groups, exclusions and semantic notes were mechanically checked without modifying them.

All fields in an entry were operative. Quoted rules can directly answer nonnumeric applications; explicit numeric applications were required for concrete arithmetic, and each supplied numeric application was independently checked. No fact was borrowed from another entry, another reader or an unattached summary passage. Support/confidence labels were ignored.

| Reader | Correct | Partial | Incorrect | Satisfied facts | Missing facts | Contradicted facts |
|---|---:|---:|---:|---:|---:|---:|
| reader-a | 96 | 8 | 0 | 317 | 11 | 0 |
| reader-b | 99 | 5 | 0 | 323 | 5 | 0 |

Unresolved required material:

- **reader-a Q026 (partial):** The entry gives ordinary rule-or-pawn access and plan timing, but no battle-plan-specific rule requirement or exclusion of pawn-only access. The Campaign passage that states that exception is not attached to this entry.
- **reader-a Q027 (partial):** The entry prohibits paying with the secret until it is flipped up, but does not state that the player’s own Rest flips it faceup. The asked ready-again timing remains unresolved.
- **reader-a Q029 (partial):** The mandatory order after site favor, Homeland and modifiers is supplied. The entry does not state the required faceup-play trigger or the absence of powers on facedown play; that conjunct is missing.
- **reader-a Q043 (partial):** The entry states the Tribunal coin-flip rule, but does not supply Tribunal’s permitted immediate favor/secret exchange or binding future actions. Generic binding-exception language does not identify those permissions.
- **reader-a Q065 (partial):** The entry says to add relevant bandits to defense, but does not identify the relevant bandits as those at targeted sites. Neither attached Overview nor Site-powers passage supplies the targeted-site defense condition; that requested relation is unresolved.
- **reader-a Q066 (partial):** No supplied passage states ruin capacity, lack of suit or ineligibility for Muster/Trade. Overview and Site powers do not contain the Components paragraph with these rules. Neither attached Overview nor Site-powers passage addresses powers printed on a ruined edifice. Continued usability under access/text is missing.
- **reader-a Q073 (partial):** Already revealed and completed at the win check is supplied. The entry does not include the ordinary reveal minor-action rule or its Act-only, not-Wake timing, so the requested attempt to reveal at Wake is not fully resolved.
- **reader-a Q081 (partial):** The entry contains Powers and Campaign passages, but no ordinary Chancellor/Citizen or Exile enemy definitions and no reciprocal bandit-enemy definition. The required enemy categories are not supplied. The specified Citizen’s temporary non-Imperial status, and the fact that others remain Imperial, are supplied. No quoted rule says that this status makes the Citizen treat every other player as an enemy. Sharing the defending side’s powers and referring to the whole side do not explicitly define your enemy as the opposing side, with defender-plus-Allies versus attacker orientation. That required relation is not stated in this entry.
- **reader-b Q027 (partial):** The entry prohibits paying with the secret until flipped up; neither its Powers nor Imperial-defense passage identifies own Rest as the readying time.
- **reader-b Q029 (partial):** The timing order and mandatory resolution are supplied, but none of this entry’s attached Powers, Site, Wake or Rest passages states that When Played triggers on faceup play rather than facedown play. The trigger-state conjunct is unresolved.
- **reader-b Q043 (partial):** Only the Tribunal disputed-breach coin flip is stated. The entry does not include the site passage describing binding immediate favor/secrets and future actions.
- **reader-b Q065 (partial):** The entry mentions adding relevant bandits to defense but does not say which sites make them relevant. Its Site-powers and Overview passages do not give the targeted-site limitation, so the required targeted-site defense relation is missing.
- **reader-b Q073 (partial):** The revealed/completed prerequisite is given, but the attached title/victory passage does not supply the normal minor-action reveal in Act or prohibit normal reveal at Wake. That asked timing conjunct is missing.


Semantic decisions: Q004’s Successor replacement conveys an exclusive Citizen win, without demanding the exact word “alone” again. Q047’s bottom-up consumption of set-aside ruins conveys reverse map order; a repeated physical collection ritual is not necessary to reproduce the ordering. Q076’s permission expressly subject to locks conveys that protected locked cards cannot be discarded. Q085’s instructions for the packet’s edifices and each suit’s stack cover all six without a redundant numeral. Q100’s optional Give permission in each direction does not impose simultaneity. These are operational equivalents, not credits for a topic label.

For Q029, the mandatory order is present but the fixed required fact also includes the faceup-play trigger. Neither entry contains that trigger or the rule that facedown cards have no power. This omission is scored partial under the supplied scope; the gold/scope has not been silently narrowed. For Q027, “until flipped up” does not answer the separately asked own-Rest timing. For Q065, “relevant bandits” does not identify the required targeted-site condition; no Campaign passage supplies that condition within either entry. For Q073, requiring a revealed Vision at the check does not itself state the Act-only reveal procedure or resolve an attempted Wake reveal.

No material contradictory application or gold/scope defect was found. Every fact has a separate status and entry-specific evidence/explanation in results.json. grading-validation.json records literal evidence/span checks, exact reconstruction hashes, fixed-artifact equality, arithmetic review and independently recomputed totals. This is an extractive, tool-assisted fixed-set regression, not an unaided paraphrase or held-out study.
