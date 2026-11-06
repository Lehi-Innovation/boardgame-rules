from pathlib import Path
p=Path('rules/ark-nova.md');s=p.read_text()
s=s.replace('base glossary and official base FAQ. This explicitly upgrades the former v1.0 extraction.','base glossary, official base FAQ and official base Icon Overview.')
s=s.replace('rulebook_version: "English base v1.2 + base glossary + official base errata/FAQ"','rulebook_version: "English base v1.2 + base glossary + official base errata/FAQ + base Icon Overview"')
s=s.replace('### ANIMALS action\n','''### ANIMALS action

**Enclosure state on animal admission:**

| Housing | Required empty space | What to do after admitting the animal |
|---|---|---|
| Standard enclosure | One empty enclosure of at least the required size | **Flip the entire enclosure to its occupied side.** It normally houses one animal. |
| Petting Zoo, Reptile House or Large Bird Aviary | At least the animal's indicated number of free special-enclosure spaces | Put that many supply player tokens on the special enclosure; **never flip** it. |

''',1)
s=s.replace('Each new Americas icon permits','Each Americas icon played permits').replace('each new Americas icon permits','each Americas icon played permits').replace('each new Europe icon permits','each Europe icon played permits')
s=s.replace('After an Animals action containing **only small animals**','An Animals action containing **only small animals** means')
s=s.replace('means, you may','means you may')
s=s.replace('**Interactive abilities.** Only zoos with at least five appeal can be affected.','**Interactive abilities.** Only zoos with at least five appeal can be affected. If the multiplayer group prefers, replace interactive abilities with the alternative text marked for solo on those cards; this does not require playing the solo mode.')
s=s.replace('- **Constriction:** place tokens','- **Constriction:** affect all other zoos ahead of yours on appeal and/or conservation. A zoo ahead on one track receives Constriction 1; ahead on both receives Constriction 2. Place tokens')
s=s.replace('- **Venom:** place tokens','- **Venom X:** affect every other zoo with higher appeal than yours, subject to the five-appeal eligibility floor. Place X tokens')
s=s.replace('Execute the targeted Action card using its owner\\\'s','Choose only a card in the target\\\'s **slot 1, 2 or 3**. Execute the targeted Action card using its owner\\\'s')
s=s.replace('- **Pilfering:** ties','- **Pilfering X:** Pilfering 1 affects the zoo with highest appeal. Pilfering 2 affects the zoo with highest appeal **and** the zoo with most conservation points. Ties')
s=s.replace('- **Pouch:** tucked cards','- **Pouch X:** you may tuck up to X hand cards under this card for **two appeal per card**. Tucked cards')
s=s.replace('- **Hunter:** add one','- **Perception X:** draw X cards from the deck, keep half and discard the rest.\\n- **Hunter X:** reveal X deck cards, add one')
s=s.replace('**Sunbathing:** sold cards go to the discard pile.','**Sunbathing X:** you may sell up to X hand cards for four money each; sold cards go to the discard pile.')
s=s.replace('even if Sponsors is upgraded.','even if Sponsors is upgraded. This paid-Sponsor effect leaves the Sponsors Action card in its current slot; it does not move it.')
s=s.replace('- Appeal cannot exceed **113**','- A left-side **maximum 25 appeal** condition permits play only while your zoo has at most 25 appeal. The matching marker at appeal 25 is a reminder, not a general track cap. An Animal partner-zoo condition means a partner from its continent; a Sponsor partner-zoo condition permits any continent.\\n- Appeal cannot exceed **113**')
p.write_text(s)
