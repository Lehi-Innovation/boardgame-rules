# Supplemental source research — John Company: Second Edition

Retrieved 2026-11-05 UTC by source-only agent. Actual model/effort: gpt-6.1-sol/high, verified from own local turn_context; see model-evidence.json. No summary, questions, keys or readers were consulted.

## Authority and provenance

Publisher resources https://wehrlegig.com/pages/resources explicitly links John Company Rulebook, Print and Play, and Official Errata. Exact HTML saved in publisher-resources.html.

The publisher-linked PNP folder is https://www.dropbox.com/scl/fo/4poovyp3gbfkgpsgaumoe/AAsIOpx2eXzsY-9EQqp6OUY?dl=0&e=1&rlkey=8a3bpbi0l1hg6g1ptvi1nbrby . Browser extraction returned no file listing, but public curl followed the folder to a complete 333,021,350-byte ZIP. Its manifest is saved in publisher-pnp-manifest.txt. Relevant original PDFs and extracted text are in pnp/. Images in images/ are rendered directly from those official PDFs; they are not independent editions or reconstructions. The file named Bridge, Bridge is in fact labelled Bridge Cards (Backs) internally. Card backs reverse front order as the accompanying A Note.txt specifies.

Crucial edition verification: publisher PNP Rulebooks/John Company Rules.pdf has exactly the same SHA256 as source_pdfs/john-company-second-edition-rules.pdf: 29fdc157234951b517190c82298ea578a543d25f183224e9fa86c1ca8c470dd0. Both state Second Printing, 2023.

Publisher-linked errata is https://boardgamegeek.com/thread/2936700/official-errata . HTML returns 403, but BGG's public API works. Saved thread metadata and all 114 unique posts in official-errata-api.json and official-errata-articles-page1.json through page5.json. API provenance is https://api.geekdo.com/api/threads/2936700 and https://api.geekdo.com/api/articles?threadid=2936700&pageid=N&sort=oldest . Complete plaintext in official-errata-thread-all-posts.txt.

Cole Wehrle's original post (author ID 11406) is https://boardgamegeek.com/thread/2936700/article/40817208#40817208 ; posted 2022-09-18, edited 2023-01-02. Saved separately in official-errata-original-post.txt. It explicitly links the full internal/public errata Doc https://docs.google.com/document/d/1hvtkMaKiyhENYW7SWNoBdGQkL-FCcSFkOycgTlaGris/edit?usp=sharing . That complete source was fetched using the Google Drive plugin and saved as full-official-errata.txt; metadata (modified 2024-04-28) in full-official-errata-provenance.json. This is the strongest direct authority chain.

Coordinator supplied two more sources, also fetched through Google Drive: https://docs.google.com/document/d/1lNCW5Jcc2ktJ8F64rhKJPMrsYP2pNLr8__Q5yt2x1i0/edit (title John Company: Second Edition - Official Errata; modified 2026-08-28) and https://docs.google.com/document/d/1S6DF8D-ODvOCKifs0fRkDqDb3thfy0rj5o9PBd4hUpc/edit (FAQ and Easily Misremembered Rules; modified 2026-11-04). Saved as coordinator-errata.txt and coordinator-faq.txt with provenance metadata. Their titles alone do not establish publication authority; no link to these two IDs appeared anywhere in the 114-post publisher-linked errata thread. Much of the former's Crown content matches Crown designer Richard Wilkins's BGG post https://boardgamegeek.com/thread/2936700/article/41627121#41627121 (author ID 136736, posted 2023-01-31, edited 2025-08-01). Do not silently promote the FAQ above contradictory designer rulings without resolving its authority.

## Exact numerical facts from the official board

Source pnp/Board/John Company Game Board.pdf, page 1. Clearly rendered evidence: images/board-left-details.png.

| Prize cost | Upkeep per pensioner | VP | Printed windows |
|---|---:|---:|---:|
| £2 | 0 | 0 | 0 |
| £4 | £1 | 2 | 1 |
| £8 | £2 | 4 | 2 |
| £14 | £3 | 8 | 3 |
| £20 | £4 | 12 | 4 |

The £2 prize has no printed upkeep, VP or window icons; zeros above describe that absence. Windows are explicit icons, not the architectural windows drawn in the painting.

Final Power Award (not a recurring end-of-turn award): final turn 1, 2 or 3 gives first/second place 3/1 VP; final turn 4, 5 or 6 gives 5/2; final turn 7 or 8 gives 8/4. Rulebook p9 supplies the tie rules.

Scenario turn track: 1710 starts turn 1 and finishes after turn 5; 1758 starts turn 3 and finishes after turn 7; 1813 starts turn 5 and finishes after turn 8. Long 1710 starts at turn 1 and may run through turn 8 (rulebook p4).

Board Power track starting positions: Social 2 power, Company shares 1 power, Shipping and Manufacturing 0 power. Evidence images/board-company-track-details.png. Standing expectations track £4/£6/£8/£10/£12/£14/£16, with Failure left of £4; reset S above £10. Lined Standing spaces above £4/£6/£8 and lined Debt spaces 5/6/7/8; stars above Standing £4 and Debt 8. These are the printed deregulation trigger spaces (rulebook p36 supplies procedure).

Orders have a large full value and small half value rounded down: £2→£1, £3→£1, £4→£2, £5→£2, £6→£3, £7→£3. Images/board-india-details.png. Rulebook p40 explains when half applies: orders previously filled this turn, rather than all orders filled by firms. No extra firm-value exception was found.

## Scenario setup cards

Official Bridge Fronts PDF page 9 has card 74 (1710), 75 (1758), 76 (1813). All text is saved in that PDF's .txt; images/cards-Bridge-Fronts-page-9.png is fully legible including outlined numerals. Matching situation-in-India diagrams are in Bridge, Bridge PDF page 9 (internally sheet 20), image images/cards-Bridge-Bridge-page-9.png. Because backs reverse the fronts, top left is 1758, top middle 1710, middle right 1813. Use these diagrams for exact towers, empire flags, closed orders, Governor overlays and Elephant position; do not infer India state solely from scenario front text.

1710: Standing above £10 expectations; Debt 0; £3 in every Company treasury; Royal Protection passed; 1 regiment in each of Bombay, Madras, Bengal armies; no starting Company ships.

1758: Standing above £12; Debt 3; £4 in every Company treasury; Calico Acts passed; 1 regiment in each army; 1 Company ship in East Indian; Bengal control token in Bengal Presidency. Diagram also supplies Governor of Bengal overlay.

1813: Standing above £10; Debt 0; £3 in every Company treasury; Military Oversight, Deregulation (Debtor's Prison side), Calico Acts passed; return Governor General LAW to box and place its overlay over Director of Trade; 2 regiments in each army; 1 Company ship in each sea zone; +2/-2 Company share VP token in Court; China office right of board; Bombay/Madras/Bengal control tokens in matching Presidencies.

Individual randomized setup cards (18 per date including six Extras) are fully present in MiniEuro Fronts PDF pages 6–9. Legible page images saved as images/player-setup-fronts-page-6.png through page-9.png (pages 10–11 are firm strategies, also rendered). Their piece icons are graphical and cannot be reliably recovered from plain text. The rulebook already supplies the dealing/drafting procedure and player count additions.

## Corrections relative to assigned Second Printing

The directly linked full errata largely describes changes ALREADY INCORPORATED in the assigned PDF: family board/loot setup p4; prestige-enterprise power p9; forced prize cannibalization and no-action rule p13; Empty Court p15 (errata mistakenly labels p14); stock exchange location p13; Shipping order and commander heading p19; Deploy targeting p22; Region Loss affiliation and Invasion-only closing p29; Elephant acting region p30; Deregulation overlay/vote treatment p36; immature shares turn timing p38; Maratha example p41; Crown AI placement after setup p44 and arrows p45. The PNP cards also include 1758/1813 setup omissions, zero-dice blackmail failure, Military Oversight old commander eligibility, Company Fraud balance floor, and Public Demands Impeachment vacancy handling.

Thus do not apply the whole first-print errata as though these were newly discovered differences from the supplied Second Printing rules.

Coordinator errata has an extra Crown p46 clarification absent from assigned p46: repeat unsuccessful checks if resources permit and no catastrophic failure, unless Handbook says otherwise. Its handbook additions/clarifications may go beyond the older full-internal-errata list. See coordinator-errata.txt and the exact Richard Wilkins living-handbook BGG post identified above.

Discarded variant: changing Crown Special Envoy cost to £3/£4/£5 by climate is explicitly struck through in Richard Wilkins's living-handbook post; his followup https://boardgamegeek.com/thread/2936700/article/42830151#42830151 (2023-08-21) says it was dropped and is an unofficial variant. Do not treat it as required errata.

## Access and interpretation gaps

No essential access gap remains for publisher-linked original errata, full internal errata, official board, scenario cards, player setup cards, Crown Handbook, player aid or letter; all were obtained. HTML-only 403 was resolved through public API; empty Dropbox browser extraction resolved through direct public download.

Authority of the two coordinator-supplied Google Docs has not yet been established through a publisher/author link. A material possible conflict exists in the coordinator FAQ's Foreign Invasion unrest statement versus a cited later designer response; see additional ruling evidence and notify the coordinator before treating that FAQ statement as definitive.

This is source research only, not an independent summary audit or reader answer key.
