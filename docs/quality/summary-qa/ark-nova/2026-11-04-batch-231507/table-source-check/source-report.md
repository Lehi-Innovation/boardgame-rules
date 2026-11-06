# Ark Nova original base action tables: source-only check

Checked 2026-11-05. Scope: supplied English base rulebook, glossary, FAQ, and extracted rules text; original blue/pink action cards. No summary, questions, answer keys, or reader material was consulted. Canonical files were not changed.

## Accepted results

All columns below are action strengths. A zero means zero; it is not an omitted entry. A printed dash in a discard row is transcribed as zero.

| Action / row | 1 | 2 | 3 | 4 | 5 | Accepted source |
|---|---:|---:|---:|---:|---:|---|
| Cards I: draw | 1 | 1 | 2 | 2 | 3 | Main rules p. 2, blue front card; corroborated by p. 8 |
| Cards I: discard after drawing | 1 | 0 | 1 | 0 | 1 | Same |
| Cards I: snap instead, number of cards | — | — | — | — | 1 | Same diagram; rules p. 9 |
| Cards II: draw | 1 | 2 | 2 | 3 | 4 | Main rules p. 2, pink front card |
| Cards II: discard after drawing | 0 | 1 | 0 | 1 | 1 | Same |
| Cards II: snap instead, number of cards | — | — | 1 | 1 | 1 | Same diagram; rules p. 9 |
| Animals I: maximum animals played | 0 | 1 | 1 | 1 | 2 | Main rules p. 8, lower example, complete Animals I card |
| Animals II: maximum animals played | 1 | 1 | 2 | 2 | 2 | Original publisher base component image, supplemented by visible main-rules p. 2 cells; see follow-up below |

Cards actions advance the break token by 2 whether drawing or snapping (rules p. 9). The draw/discard rows do not apply when snapping. Animals II at strength 5 or greater also permits gaining 1 reputation at the beginning of the action (rules p. 13); the p. 2 card shows that icon in its strength-5 cell.

**Follow-up resolution:** Animals II strengths 1, 2, and 3 are covered in supplied rules p. 2. They are now supported by an independently inspected [original Feuerland base-game component image](https://www.feuerland-spiele.de/fileadmin/game/Arche_Nova/Spielzene.jpg), also reproduced on the [2021-copyright box back](https://www.feuerland-spiele.de/fileadmin/game/Arche_Nova/Back_arche_nova.jpg). Both are linked as product-image downloads from the [publisher's original base-game page](https://www.feuerland-spiele.de/spiele/arche-nova/). The complete pink giraffe card prints 1, 1, 2, 2, 2; its visible strength-4 and strength-5 entries match the English illustration exactly. This is explicitly a **German-language original component supplement**, not direct observation of the covered English cells or adoption of German revised rules. The canonical English sources remain unchanged. See `followup-source-report.json` for the comparison, source hashes, native crop coordinates, acceptance rationale, and language/version boundary. No numeric table gap remains when this supplemental original-component evidence is accepted.

## Local evidence and extraction method

- `local-rules-page-2-embedded.jpg`: first embedded image from PDF page 2, 1243 × 1754 pixels. `local-page-2-action-cards-crop.png` crops rectangle (500, 500, 1180, 690), then enlarges 4× for inspection. It preserves the covered Animals II cells.
- `local-rules-page-8-embedded.jpg`: first embedded image from page 8. `local-page-8-action-cards-crop.png` crops (640, 650, 1150, 800), then enlarges 4×. The complete Animals I table is visible.
- Additional embedded page images and `local-rules-all-pages-embedded-contact-sheet.jpg` document inspection for another unobscured upgraded card. These are embedded artwork extractions, not full PDF renders; body text is absent from those images. Body rules were checked in the permitted extracted text and PDF text.
- `evidence-manifest.json` records SHA-256 hashes for the supplied PDFs and saved evidence.

## Publisher downloads and provenance

The [official Capstone Ark Nova product page](https://capstone-games.com/products/ark-nova/) links its rulebook and icon overview separately from its teaching guide.

1. [Capstone rulebook](https://capstone-games.com/cdn/shop/files/Ark-Nova-Rulebook.pdf?v=15269496103518830006), saved as `capstone-current-rulebook.pdf`. It is **byte-identical** to supplied `source_pdfs/ark-nova-rules.pdf`: SHA-256 `f6b4eedc68e993f61b4c5cb5d99bb4af399da0be3de4781321bcba1ba44516f6`. Thus this download adds provenance but no new table visibility.
2. [Capstone Icon Overview](https://cdn.shopify.com/s/files/1/0947/3907/1278/files/Ark-Nova-Icon-Overview.pdf?v=1754428545), saved as `capstone-icon-overview.pdf`. Page 2 includes original side-I action tables in examples and corroborates Cards I and Animals I. It does not supply the missing Animals II cells. Extracted images beginning `icon-overview-` are preserved from this inspection.
3. Publisher product photographs linked from that product page are preserved as `imgi_*` files with a contact sheet. They show the revised action-card layout and are **excluded** from numeric rules authority for the original-layout check.

## Excluded teaching guide

`capstone-current-strategy-guide.pdf` was downloaded from the product page's “How To Play – Guide” link before the parent clarified that the user's source restrictions explicitly exclude strategy guides. It and all files beginning `guide-` are retained solely to document that rejected path. They must **not** be cited to establish any answer-key value, even where a card picture appears inside the guide. The earlier provisional message claiming that this guide resolved Animals II is withdrawn for accepted-source purposes.

Excluded URL: https://cdn.shopify.com/s/files/1/0947/3907/1278/files/Ark-Nova_StrategyGuide_V1_Web_Updated_5.1.26.pdf?v=1777649815 . Its PDF metadata gives creation 2024-12-17 and modification 2026-05-01. These dates do not establish base-rule authority.

The older guessed Capstone start-guide URL returned HTTP 404 and was not saved. No Marine Worlds rules or alternate action cards were used.
