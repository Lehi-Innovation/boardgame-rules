# Focused original-core Range clarification

Verified 2026-11-05 UTC. No summary, questions, keys, readers, grades, or other reviewer reports were read or edited for this clarification.

## Source captures

1. Official Living FAQ, **If I get a Range boost, what Ranges does it affect?**
   - URL: https://querki.net/raw/darker/spirit-island-faq/What-do-range-boosts-affect
   - Raw primary: `what-do-range-boosts-affect.html`; complete derived text: `what-do-range-boosts-affect.txt`.
   - Capture: 2026-11-05T16:15:44.301627+00:00.
   - Raw HTML SHA256: `3fd917155f8ad3f898b634a149b081bb63f506fe568a27250fb78f065cb461d9`.
2. Original printed **Reaching Grasp** face:
   - URL: https://sick.oberien.de/imgs/powers/reaching_grasp.jpg
   - Primary face: `reaching_grasp.jpg`.
   - Capture: 2026-11-05T16:15:51.965122+00:00.
   - SHA256: `def3a446b182cef25e29663e1cdb0bc7c9e1acb301950489f34ab4e0f2ff26ef`.
3. Official Living FAQ, **Where is Range in the text of a Spirit-targeting Power measured from?**
   - Exact question located through the official Range index: https://querki.net/raw/darker/spirit-island-faq/Range . Captured as `faq-range-index.html` solely to preserve the direct entry locator.
   - Entry URL: https://querki.net/raw/darker/spirit-island-faq/range-in-text-of-powers-that-target-spirits
   - Raw primary: `range-in-text-of-powers-that-target-spirits.html`; complete derived text: `range-in-text-of-powers-that-target-spirits.txt`.
   - Capture: 2026-11-05T16:17:50.513416+00:00.
   - Raw HTML SHA256: `aa79f3892c1c67d67529cce3f8e1b1111ede8da3a81f75ba6f041c314885767b`.

Full URLs, dates, byte counts, and SHA256 values are appended in `provenance.jsonl`; all preceding records are preserved.

## What the primary FAQ establishes

The range-boost entry requires all four conditions: the action belongs to the Spirit receiving the bonus; the relevant Range has a printed arrow; that Range is **“not itself a Range boost”**; and any restriction on the bonus still applies. Accordingly, a general bonus can reach arrows in effect text as well as the targeting box, but it does not increase a bonus being granted. It also does not affect Powers used by another Spirit, even when those Powers target the boosted Spirit. The exclusions for Gather/Push and wording based on Presence/ownership rather than a printed Range arrow are explicit, rather than inferred from examples.

An unqualified “general Range boosts apply to all numeric Range arrows in a Power” therefore needs the not-a-Range-boost exception for original-core play. It also needs ownership and any source/target restrictions preserved.

The source's final paragraph mentions an expansion card's wording revision. That paragraph is not needed for this core result and does not establish expansion membership. No expansion example is imported into the recommendation below.

## Original core Reaching Grasp

The full original-layout face was visually inspected. It has **no expansion mark**, consistent with the previously captured official B&C p.6 marker legend. Its metadata is cost 0, Fast, any Spirit target; its targeting Range box contains a dash rather than a numeric land-targeting range.

Printed effect, transcribing the arrow as a bracketed icon:

> Target Spirit gets +2 [Range arrow] with all their Powers.

The **plus sign** is visibly printed above the arrow together with the numeral 2. This is a grant of a Range bonus, rather than an ordinary Range value from which to measure a particular target. Thus another Range boost does not increase the +2 amount granted by Reaching Grasp. This is a direct original-core reason to retain the qualifier.

Identity correction: the request called Reaching Grasp a Unique of A Spread of Rampant Green. The card locator at `catalog-cards.js:1087` identifies it as a **base Minor**, not a Unique. The primary FAQ separately tags Green's **Gift of Proliferation**, which is a different card. The original face proves the printed name and effect; its deck subtype is corroborating catalog metadata rather than a printed subtype label on this face. Do not propagate the requested Unique attribution.

## Internal arrows on Spirit-targeting Powers

The second FAQ explicitly separates the **origin of the measurement** from **ownership of the Range bonus**:

- Unless the Power states otherwise, measure the internal arrow from the Presence of whichever Spirit follows that instruction, usually the target Spirit.
- Apply the Range bonuses of **“the Spirit using the Power”**, even if a different Spirit supplies the Presence from which Range is measured.
- The entry specifically identifies **Blazing Renewal** as an explicit exception to the default measurement origin: it measures from the Power user's Presence even when another Spirit adds Presence. Its original core face is already preserved as `blazing_renewal.jpg`, and visibly specifies the user's Presence.

The second entry's product tags list Jagged Earth / Feather & Flame / Promo, but its tags explicitly include core **Blazing Renewal** and **Gift of Proliferation (A Spread of Rampant Green)**. This is a general mechanics clarification, not evidence that either core card belongs to those expansions. The rule text above is explicit primary FAQ text; it is not an inference from those product tags. No additional procedure concerning either card is imported here.

Suggested compact core formulation: **General Range boosts affect printed Range arrows in Powers you use, including effect-text arrows, subject to all restrictions; they do not increase a Range boost or affect another Spirit's Powers. For internal Range on a Spirit-targeting Power, measure from the instructed Spirit's Presence unless specified otherwise, but use the Power user's Range bonuses.**

## Reading and formatting checks

- `what-do-range-boosts-affect.txt`: all 2290 characters read in one bounded output; explicit completion check true. Complete relevant HTML `.querki-content` element, 3626 characters, also read without truncation. Checked paragraph boundaries, the three exclusion bullets, emphasis on each “not,” and the link on targeting-only restrictions. The not-itself-a-boost condition is in the opening paragraph, not an editorial addition.
- `range-in-text-of-powers-that-target-spirits.txt`: all 1325 characters read in one bounded output; completion true. Complete `.querki-content` element, 2409 characters, read without truncation. Checked default-origin paragraph, the two example bullets, and the link from bonus ownership back to What-do-range-boosts-affect. “The Spirit using the Power” is the source anchor text, not a replaced pronoun.
- The complete 300×420 Reaching Grasp face was viewed without cropping or truncation; the +2 arrow, nonnumeric targeting box, full effect, and both lower corners are visible.
- No relevant source output exceeded 6000 characters. The Range index was searched only for bounded locator anchors, not read as an unrelated FAQ corpus.
