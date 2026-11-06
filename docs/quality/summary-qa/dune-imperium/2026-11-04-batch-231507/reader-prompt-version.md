# Reader prompt versions

V1: guide-plus-self-check-v1 was used for seed iterations1–6 and expanded iteration03. All those readers ultimately received complete frozen summaries and question texts: per-iteration input-read-audit.json and actual read traces show recovery after initially truncated combined reads where applicable. No run was invalidated solely because its first read was truncated.

V2: guide-plus-self-check-v2-bounded-reads is used from expanded iteration04 onward. It adds only this generic file-reading guidance, with no game facts, key hints or earlier findings:

> Read the two inputs separately in bounded chunks (for example, no more than 60 lines per tool call). Do not combine both whole files into one output. Inspect each result for truncation; if any output is truncated, reread the missing ranges in smaller chunks until you have seen both complete files before answering.

Both versions retain the local guide’s two-input restriction, fresh fork_turns=none, gpt-6-luna/high, strict grading, no sources/key/history/browsing/prior game knowledge and this unchanged generic pre-submission check:

> Before writing final JSON, reread every question and review your draft answer on your own; explicitly resolve every requested part from the supplied summary, including requested quantities, timing, costs, destinations and exceptions; do not borrow a missing fact from another answer; identify unsupported parts instead of guessing; check volunteered rulings for contradictions with the summary.

Per-reader dispatch.json files preserve intended exact authored spawn bodies. Runtime parent spawn arguments confirm model/effort/fork settings; child turn_context confirms actual models and effort. Task bodies are encrypted, while environment-only runtime user-message captures are accurately labeled and not represented as recovered task prompts. Actual input tool calls/visible outputs are inspected for completeness. Support labels are not grades.
