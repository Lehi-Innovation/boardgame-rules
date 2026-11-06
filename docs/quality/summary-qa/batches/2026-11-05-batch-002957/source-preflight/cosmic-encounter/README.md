# Original Cosmic Encounter component source packet

The normative additions are the **50 printed FFG alien-sheet facsimiles in
`alien-sheets-original/`**, uploaded to the public component-image archive between
October 2009 and February 2010. Their exact paths, dates, dimensions, archival
SHA-1 and local SHA-256 values are in `original-alien-sheet-provenance.json`.
All 50 match the archive's original byte length and SHA-1.

The images show the original FFG artwork, complete power text, alert lamps,
usage roles, mandatory/optional status and timing bars. The coordinator inspected
Fido and Virus as samples. The game worker and independent final source auditor
must inspect every assigned sheet; sample inspection does not replace that work.
Apply the separately assigned official base-game FAQ where it corrects a sheet.
Do not treat the community wiki's prose or a fan transcription as rules authority.

`fandom-category-response.json` and `fandom-imageinfo-response.json` preserve the
public MediaWiki API's component index and original-image metadata. The source
category also contains expansion sheets; only the explicitly assigned original
50 images are in scope. `base-alien-list-community-lead.json` records navigation
and identity information from a public workshop's Base Aliens object. That
community list is not authority for the rules printed on the sheets.

The image CDN initially supplied WebP derivatives, preserved in `alien-sheets/`.
The `format=original` responses, preserved in `cdn-original-format/`, supplied JPEG
bytes with their JFIF density header stripped. Inserting the recorded 18-byte
300-dpi JFIF APP0 header after SOI recovered the **exact original archival bytes**
for all 50 files. Acceptance required both the archive's byte length and SHA-1;
no image was decoded and re-encoded. The provenance records every transport hash
and the exact inserted header. The two CDN derivatives are not assigned authority.

The public workshop metadata, page, original BSON and bounded decoder are kept
as discovery history. Its base-component references point to licensed local DLC
asset names, not public image URLs. No DLC was accessed, no workshop script was
executed, and no fan script supplies a rule. The original printed scans were
retrieved independently from their public image archive.

Individual flare effects remain printed components. Source any specific effect
asserted in the summary; do not infer it from a fan description. The worker brief
retains the complete base encounter/alien/flare system scope and excludes later
editions, expansion aliens and optional modes explicitly.

`navigational-ocr/all-fifty-navigation.txt` and its per-image files offer a
searchable navigation aid. `navigational-ocr/manifest.json` records each original
image and OCR hash. All original images remained unchanged. OCR can misread
numbers, restrictions and graphical timing bars; it is not a replacement for
reading every native image or checking a claimed rule against its printed sheet.
