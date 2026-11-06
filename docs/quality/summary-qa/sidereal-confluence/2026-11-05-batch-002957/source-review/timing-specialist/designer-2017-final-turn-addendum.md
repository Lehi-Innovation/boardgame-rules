# Contemporaneous designer clarification addendum

This source-only addendum supplements `source-timing-report.md`. It changes the evidence status of the final phase order and final Zeth theft from application of general booklet/sheet rules to **direct, explicit original-designer clarification**. It does not change the resulting timing ruling. No summary, answer key, reader submission or reader feedback was accessed.

## Primary-source acceptance

**Accepted, high confidence, for the original 2017 game.** Both posts are direct original API articles by author ID **1220373**, not another user's quotations of the designer. The preserved author API profile identifies that stable ID as **TauCetiDD / TauCeti Deichmann**, links designer ID **25517**, and carries the board-game designer badge. The name matches the assigned 2017 booklet p10 game-design credit.

- [Article 26690049](https://boardgamegeek.com/thread/1833405/article/26690049#26690049): posted **2017-08-20 14:51:58 UTC**, edited **2017-08-20 14:53:02 UTC**; raw pointer `/articles/0/body` in `thread-1833405-articles.json`.
- [Article 26803262](https://boardgamegeek.com/thread/1840710/article/26803262#26803262): posted and edited **2017-09-01 11:31:56 UTC**; raw pointer `/articles/3/body` in `thread-1840710-articles.json`.

The original dates and edit dates are contemporaneous with the assigned booklet and original printed components and precede the excluded 2020 edition. Article 26690049 explicitly discusses the same “Scoring-Only Economy” wording on the original Confluence-card reverses and the exact six-turn ambiguity under review. Article 26803262 supplies an explicitly official answer for Zeth's last turn. No later-edition procedure is needed to interpret these statements.

All **five manifest-bound files** passed independent SHA-256 checks: both raw thread API files, the profile API file, and both complete author-text derivatives. Both derivatives were independently regenerated from their raw article bodies using the documented BeautifulSoup transformation and matched exactly. The thread files contain **6 of API total 6** and **5 of API total 5** articles respectively. Although the requested URLs specify `perPage=100`, the returned API metadata says `perPage=25`; both totals are below 25, so this does not truncate these preserved API result sets. The packet's own provenance file was also read completely and its actual hash recorded; it has no separately supplied expected self-hash.

These checks independently validate the supplied preserved primary API packet; no remote refetch was performed. Details, full hashes and complete bounded character-read receipts are in `designer-addendum-verification-receipts.json`.

## Supported final-turn procedure

Article 26690049 directly states this order for **Turn 6**:

1. **Trade:** trade and invent the game's last technologies.
2. **Economy:** run economic converters under their normal printed limits and species exceptions. “Scoring-only” means this production has no later Trade Phase in which to use it for invention; it does **not** suppress production or authorize economic chaining.
3. **Confluence:** receive the technology-sharing victory points, then end **before bidding begins**. Neither the colony bid nor the research-team bid occurs.
4. **Zeth, if present:** article 26803262 expressly places the final theft **immediately before counting score**. In conjunction with the direct phase sequence, this is after the final Economy and sharing and before resource conversion/counting.
5. **Score:** apply the leftover-resource formula to all remaining qualifying resources and ships.

This explicitly confirms that final Trade inventions are shared **after** the final Economy; they do not reach other players before that Economy through ordinary Confluence sharing. Special abilities such as Yengii licensing remain governed by their own printed rules. There is no seventh turn, extra Trade Phase, extra Economy Phase, or final bidding round.

Article 26690049 also directly confirms that the last Economy's donation goods remain with their producers. Turn 5's Economy is the final production that can supply resources for a later invention opportunity; Turn 6 Economy outputs cannot fund another invention or another economic converter.

## Input colors and output colors

- **Final Economy inputs must still have the correct colors.** Article 26690049 explicitly preserves this requirement. Correct sizes alone are insufficient for fixed-color input costs; normal printed wild-resource permissions still apply.
- **Final Economy outputs may use arbitrary colors of the correct size for ordinary final scoring.** The color shortcut affects produced goods, not the resources paid as inputs. Economic simultaneous-production restrictions remain unchanged.
- **Zeth must actually be entitled to the correct-colored inputs for a final stealing converter.** Article 26803262 explicitly identifies theft as the exception to the end-game output-color convenience: Zeth cannot exploit substituted-color output pieces to claim inputs they would not really have. Its observation that these colors are usually black is descriptive, not permission to replace every printed stealing cost with black.
- The exception concerns paying the stealing converter. It does not repeal the Zeth sheet's separate rule that the goods stolen depend on size/shape rather than color, nor its immunity for Unity wild cubes.

Practical supported implication: retain the actual output colors, or an unambiguous accounting of them, for Zeth's resources that may pay final theft. A same-size shortcut piece is not evidence that its substituted color was truly produced. This implementation advice is an implication of the designer's correct-color restriction, not a new component rule.

## Scoring-arrow repeatability

The booklet p9 / original final card formula applies to **all** leftovers: each octagon, each complete pair of large cubes, and each complete group of three small cubes and/or ships contributes **½ point** under normal scoring. For example, six small cubes/ships produce two such groups and therefore 1 point; four large cubes similarly produce 1 point. Resource colors do not affect these conversions.

The assertion that these arrows should escape the normal once-per-turn converter restriction appears first as **rayuffrahst's quotation** inside article 26690049. That fan quotation is not independent authority. The designer's own following response explicitly confirms it and explains that the Confluence-card arrows are merely reminders of the scoring formula. The supported ruling is therefore **apply the scoring formula for every qualifying group**, not one use of each pictured arrow. This confirmation does not make ordinary economic converters repeatable.

This addendum does not replace the booklet's separately labeled optional precise-resource-scoring rule with a new formula. Its repeatability finding concerns the normal end-game formula printed on the card and described in p9.

## Official ruling versus optional or quoted material

- In article 26803262, the opening official ruling is unequivocal: Zeth steal on the last turn and do so last before scoring. The closing observation that a group could house-rule theft either way is an **optional house rule**, not a reversal of that official answer. Advice about paying only a ship or two for final-turn protection is strategy, not a cost limit or new protection rule.
- Article 26803220, by author ID 267252, quotes the designer in another user's post. It was read for context but is not used to establish authorship or the timing rule; the full original article 26690049 was independently verified instead.
- Other users' assumptions, proposed flowcharts, anecdotes, and interpretations in either thread are not official rulings. In particular the fan flowchart that labels Turn 6 simply Trade → Economy → Final Scoring does not override the designer's explicit final sharing Confluence.

## Remaining source limits and delivery

No consequential ambiguity remains in the requested final timing, ordinary input/output color handling, scoring-formula repeatability, or official final Zeth timing/color requirement after these direct rulings. Article 26690049's broad shorthand about produced resources being useful only for scoring is qualified by the later direct Zeth ruling when Zeth is present; the latter explicitly addresses final theft and its correct-colored cost. This is a specific clarified exception, not authority for extra economic chaining or last-minute invention after the Economy.

The previous source report is preserved unchanged. Its labels describing final sharing order and Zeth theft as inherited conclusions should now be read together with this addendum's direct primary-source confirmation. The original booklet, species sheets, component atlas/crop provenance, and all new packet files remain untouched. Only this specialist output directory was written.

Delivered: `designer-2017-final-turn-addendum.md` and `designer-addendum-verification-receipts.json`. The coordinator received a progress receipt identifying the official rulings and optional-house-rule distinction. No information was sent to blind readers.
