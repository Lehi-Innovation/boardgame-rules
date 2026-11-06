# Unadopted read-call JavaScript format proposal

This separate proposal addresses a narrow representation mismatch: the frozen proof currently recognizes exact outer JavaScript spellings, even when another whitespace spelling represents the same fixed shell read command. It does not change any existing proof, helper, runtime, grade, factual score or denominator. **An independent fresh technical reviewer must assess this proposal before any future actual use.** No actual runtime or `prove()` execution was performed here.

## Accepted grammar

`read_call_format_proposal.py` recognizes only this complete body, with ASCII JavaScript whitespace between permitted tokens:

```javascript
const r = await tools.exec_command({cmd: "JSON string" + "optional second JSON string", max_output_tokens: 24000});
text(r.output);
```

The concatenation is optional and permits at most two static JSON double-quoted string tokens. `cmd` and `max_output_tokens` may optionally be quoted with those exact double-quoted names. Key order, identifier names, decimal budget `24000`, both statements and semicolons are fixed. Whitespace is required between `const` and `r`, and between `await` and `tools`, to avoid recognizing invalid merged identifiers. Spaces, tabs, LF, CR, vertical tabs and form feeds are the supported whitespace set.

The parser anchors the whole body. It accepts no dynamic variable, template literal, interpolation expression, function, call expression, additional operator, third literal, computed key, getter, spread, prototype field, duplicate field, extra argument, changed budget, trailing comma, extra semicolon or extra statement. Ordinary comments are rejected. Strings containing code-looking text, comment markers, `${...}`, shell metacharacters or quotes remain literal **data**; their presence does not execute anything or turn them into source syntax.

Only JSON escapes are accepted. Raw control characters and raw U+2028/U+2029 are rejected; the latter may appear through JSON escapes. Lone surrogate code points are conservatively rejected by normalization; a valid escaped surrogate pair is supported. Single-quoted JavaScript strings, JavaScript-only escapes and other otherwise-valid JavaScript constructions remain outside this deliberately small language. Quoted keys using escaped letters are also outside it. This is neither a sandbox nor a full JavaScript grammar.

## Normalization is not approval

The parser decodes only the string token(s), statically concatenates their values and reconstructs exactly:

```python
'const r = await tools.exec_command({cmd: ' + json.dumps(command) + ', max_output_tokens: 24000});\ntext(r.output);'
```

This matches the original `literal_read_call` template. It does not tokenize or normalize the shell command, run JavaScript, evaluate an expression or execute a shell. Different JSON escape spellings may represent the same static command; the resulting command value must remain exactly equal, including all shell whitespace and quoting. For valid Unicode strings, equal command strings imply equal UTF-8 command bytes.

The original proof still constructs its allowlist from its fixed `READ_SCRIPT`, the two frozen allowed paths, the permitted modes and exact indices. Both the whole-literal and prefix-plus-suffix representations already have entries in that frozen allowlist. Only exact canonical-body membership grants approval. A parser-recognized command with a changed script, path, mode, index, shell spacing, extra shell command or trailing whitespace remains unapproved. The new parser never chooses paths, routes questions, infers coverage or adds allowlist entries.

## Wrapper and inherited behavior

`load_proposal_proof()` reads and hashes only the two permitted generic proof sources, refuses versions differing from the embedded reviewed hashes, imports the original module and overrides **only its in-memory `call_body` function**. The original source files are untouched. Other proof functions retain their identities; neutral tests check this explicitly.

The replacement first calls the original `call_body`. This preserves the original stripping and its pre-existing leading `// @exec:` preprocessing exactly. That one inherited directive is an explicit exception to the no-comment grammar above; the new parser itself strips no comments. An ordinary leading comment, inline comment or added statement remains unrecognized. On a parse failure the original body is returned unchanged, preserving existing exact approvals and unknown-call handling rather than guessing a repair. The original leading-pragma implementation's malformed-input behavior is also inherited, not expanded into a general comment parser.

The first-write marker is not parsed or reconstructed. A marker-bearing write body remains byte-for-byte equal to the original `call_body` result. The original session reader still records the original raw input for audit, binds outputs to call IDs, rejects unknown pre-boundary calls, tracks missing/duplicate IDs and unmatched outputs, credits no post-write output as initial delivery, records status/other-agent calls and retains post-boundary calls for the separate audit. The exact source/output/entry comparisons, frozen-input hashes, approved-object walker, truncation/recovery handling and complete-delivery predicate are unchanged. They were exercised only with neutral traces; no actual frozen packet or provenance was inspected.

`prove(..., output_name=...)` is a future-use API with no default output name. It accepts only an explicit new `*-js-format-proposal-proof.json` basename and delegates to the unchanged original `prove`. Its existing exclusive `open('x')` remains in force, so existing proof results cannot be overwritten. The original strict/false result must be retained, with any future reviewed comparison saved separately and bound to these proposal/source hashes. There is no command-line runtime execution entry point. Tests call this API only with a stubbed loader/prove; they never invoke actual `prove`.

Source hashing is version binding, not protection against a concurrently modified filesystem or arbitrary Python callers. The lower-level parser/installer are reviewable helpers, not a capability boundary. Any later source change requires another review. Existing post-write arbitrary code still needs the original separate permitted-path/isolation audit. This proposal does not certify that audit, attention, source comprehension or factual correctness.

## Neutral tests and evidence

Run from this proposal directory:

```sh
python3 -B fixtures/test_proposal.py
```

The suite imports only the two allowed generic proof files and this proposal. It writes synthetic trace/result artifacts only below its own `fixtures` directory. The neutral trace inputs are never executed: they are JSON strings passed to the frozen session parser. No actual shell read command, JavaScript code, source/packet data, runtime, provenance or grade is opened. Some synthetic dictionary keys mirror the generic proof's entry shape solely to test unchanged equality handling; their contents are newly authored neutral placeholders.

Positive cases cover compact/expanded/newline/CRLF/tab formatting, quoted exact keys, one or two literals, equivalent JSON escapes, valid Unicode and code-looking literal content. Negative cases cover malformed strings, ordinary comments, dynamic/interpolated/function expressions, duplicate/prototype/computed fields, changed numeric syntax/budgets, extra calls/statements and invalid merged keywords. Integration cases cover exact command allowlisting, raw-input preservation, first-write/late-output/post-write behavior, unknown/status calls, missing/duplicate/unmatched call IDs, changed source/entry values, truncation and recovery. A neutral path containing code-looking characters is still approved only when its entire fixed command is precomputed in the neutral allowlist.

One deterministic property case additionally checks 256 generated static literal pairs containing quotes, backslashes, controls, Unicode and code-looking data, plus 512 extra-syntax rejection mutations. Its seed and generator are saved in the fixture code; it performs no semantic or gameplay evaluation.

`fixtures/neutral-results.json` and `fixtures/execution.json` record final test results. `sha256-manifest.json` binds both permitted generic inputs and all proposal artifacts, excluding itself to avoid a recursive hash. The wrapper's future `prove` forwarding is tested using a stub; no actual end-to-end proof, current proof correction or grading change is claimed. Known limits are the intentionally narrow grammar and all inherited proof/audit assumptions. No failing neutral test or implementation defect remains identified by this author's suite; independent fresh review is still required.
