# Frozen technical prefix audit

Frozen at 2026-11-06T08:37:23.024015+00:00. Technical findings only; no factual grading or score cap.

Both readers visibly received every one of the 492 physical LF source lines and all 116 complete question objects before any possible output write. Exact outputs were compared against their executed source slices and recovered JSON objects. Both oversized whole-question attempts were transport-truncated and fully recovered in 20 responses of at most six objects each. B additionally printed 87 source lines in its last initial summary response, exceeding the 45-line cap without losing content.

A froze through physical record 259, with Q001–Q002 individually saved in its draft and self-check; Q003 had been reread. Each saved entry followed one-question and full T079 receipt. Its heading metadata drops the literal ### prefix, compound requested fields remain grouped, and mechanical True flags were hardcoded rather than compared. The source slice/hash itself matches. Its final output was absent.

B froze through physical record 255. After only Q001 reread and complete I079 receipt, record249 attempted a prefilled 116-question routing map and whole-bank answer/check generator, including regex-generated clause maps and case defaults. This violates the sequential individual method. The generator failed before writes with a visible TypeError at record252. All three B output files were absent; the attempted map is not a completed answer bank.

Both readers called collaboration.send_message to /root before completion (A218; B234), a procedural deviation. Message bodies are omitted. All filesystem paths in observed code were assigned inputs or each reader own outputs. Actual narrow runtime metadata confirms gpt-6-luna/high for both, with the expected parent and agent identity.

First five completed entries were unavailable at freeze. Findings apply only to these hashed prefixes and own-file raw-byte hashes; later work is outside scope. No reader was contacted, graded, repaired or stopped.

Artifacts: audit.json; input-and-prefix-hashes.json; actual-initial-delivery-checks.json; actual-runtime-a-projection.json; actual-runtime-b-projection.json. Original raw runtimes were not copied. Saved projections exclude all full metadata/context/message/reasoning/encrypted bodies. One exploratory tool print inadvertently exposed an encrypted call argument outside repository artifacts; it was reported to root and omitted from every saved projection.
