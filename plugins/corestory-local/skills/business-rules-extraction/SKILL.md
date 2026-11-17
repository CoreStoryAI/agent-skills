---
name: business-rules-extraction
license: MIT
description: "Extract, document, and source-verify the business rules in a codebase that CoreStory has ingested, and write them to a rules inventory file. Use when asked to extract, document, list, or inventory business rules, calculations, validations, authorization, or state transitions for a module or domain."
---

# Extract business rules into an inventory file

Output: `RULES.md` in the repository root (or the file the user names). Create it at the start and append as you go.

## 1. Preflight

Call `status`, then `corpus_info`. Proceed only if `status.state` is `snapshot_selected`, the latest ingest has not `failed`, and the `sao:Rule` count is above zero. Otherwise stop and relay `status.next_step`. Never call `init` or `ingest` without the user's explicit OK; `ingest` spends their model-provider money. If `search` says it "could not answer", the embedding key is missing: use `rules_for`, `entity`, `connections` and `read_file` instead.

## 2. Scope

Restate the scope in one line at the top of `RULES.md`. If it is broad and you can ask, ask for one module or domain. If you cannot ask, take the narrowest reasonable reading and record it.

## 3. Find the rules

- Concept sweep: `search(query, kind:"sao:Rule")` for each concept in scope (calculation, validation, authorization, state change, defaults, limits). Default limit. Hits are leads: `search` never returns empty.
- File sweep: for each program or file the hits point to, call `rules_for(path)` and follow `next_call` to the end. This finds rules the concept sweep missed. It also returns rules that only support those lines, so check each.
- For each rule that matters: `entity(entity_id, include:["description","evidence"])`. This gives the statement, typed values, the verbatim quote and the line span.

## 4. Verify against source

`read_file(path, start_line, end_line)` on every evidence span before it goes in the inventory. Confirm the quote or condition is on those lines. Then:

- Enforcement point: find where in the execution path the check runs or the update is made, not just where a value is declared. Record what happens on violation (rejects, abends, clamps, ignores, logs and continues).
- Declared but not enforced: a field, constant, or check that nothing reads or that cannot be reached. Mark it `declared-not-enforced`, never as a rule.
- Scope: say if the rule holds on every path, on some, or only in one screen or job.
- Values: copy literals, rates, divisors, thresholds, and table entries from the source lines, not from a summary. Rules that depend on a lookup table or data file: read the table.

## 5. Trace flows

For the main entry points in scope (a batch job's main paragraph, a transaction handler), read the path from input to final write, using `connections` on the program entity for call edges and `read_file` for the code. Look for ignored input, overwrites where the name suggests adding, swallowed errors, defaults that mask failures, and updates that happen in an order or place the rules did not mention. Add behavior the graph did not give you as new rules with `source: flow-trace`.

## 6. Write the inventory

Header: scope, date, build (`corpus_info` snapshot id). Then one block per rule:

```
### BR-001 short-name
- Claim: one plain sentence
- Category: calculation | validation | authorization | state-transition | default | limit | other
- Evidence: `path:start-end` — `short quote from the lines`
- Enforcement point: `path:line` and what happens on violation
- Values: literals, rates, thresholds, with their source lines
- Status: confirmed | corrected | declared-not-enforced | uncertain
- Notes: how it differs from the graph's statement (if corrected), CoreStory rule id (if any), source: graph | flow-trace | source-search
```

Group by category. Add a table of `declared-not-enforced` and `uncertain` rules with the reason.

End with `## Not verified`: rules you did not read back against source, files or flows you did not reach, paginated results you did not exhaust, constructs the graph has no structure for, and that the graph describes the ingested snapshot, not necessarily the working tree. An empty or exhausted `rules_for` does not mean a file has no rules.

Do not call the inventory complete. CoreStory indexes and quotes code; it does not run it, so do not say CoreStory tested any behavior.
