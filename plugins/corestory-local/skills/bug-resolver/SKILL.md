---
name: bug-resolver
license: MIT
description: "Find the root cause of a defect with CoreStory v3 rule evidence, fix it test-first, and write the investigation to BUG-NOTES.md. Use when asked to fix a bug, regression, wrong result, failing behavior, or a bug ticket in a codebase CoreStory has ingested."
---

# Resolve a bug

> On hosted CoreStory the tools are prefixed `v3_` (e.g. `v3_rules_for`), take a `project_id` (from `list_projects`), and there is no `status`/`init`/`ingest`: start with `v3_corpus_info`. When following a `next_call`, use the `v3_` name and the same `project_id`.

Output: `BUG-NOTES.md` in the repository root (or the file the user names). Create it first and append as you go. Do not create a ticket, commit, push or publish unless the user asks.

## 1. Preflight

Call `status` if available, then `corpus_info` (hosted: `v3_corpus_info` for the chosen project). Proceed only if `status.state` is `snapshot_selected`, the latest ingest has not `failed`, and the `sao:Rule` count is above zero. Otherwise say CoreStory evidence is unavailable, relay `status.next_step`, and ask whether to continue from source alone. Never call `init` or `ingest` without the user's explicit OK; `ingest` spends their model-provider money. If `search` says it "could not answer", use `rules_for`, `entity`, `connections` and `read_file`.

## 2. Symptom

Write the symptom, expected behavior, where it shows, and how to reproduce it at the top of `BUG-NOTES.md`. If you can ask for missing details, ask. If you cannot, state your assumptions in the file.

## 3. Investigate

- Rules about the behavior: `search(query, kind:"sao:Rule")`, then `entity(entity_id, include:["description","evidence"])`, then `read_file(path, start_line, end_line)`. Hits are leads; `search` never returns empty.
- Code path: `search(query)` for the symbols and files, `connections` on an entity for callers and callees, `list_files(prefix)` for nearby tests, `read_file` for the lines.
- Hypothesis: write the leading cause and one or two alternatives, each with the `path:start-end` you read.

## 4. Cross-layer concept sweep (required before any edit)

The same value or rule is often enforced in more than one layer, and the file with the symptom may not be the one that decides it.

1. List the business nouns and quantities the symptom touches (amounts, counts, thresholds, dates, statuses) in the notes file.
2. For each, run `search(query, kind:"sao:Rule")` with at least two plain-language phrasings of the concept, default limit. Do not paste the ticket text.
3. Open with `entity(entity_id, include:["description","evidence"])` every hit whose file is not one you plan to edit and whose statement constrains the same noun or quantity, then `read_file` the evidence lines.
4. Record each as `constraint from another layer: path:start-end, value`, across services, entities, config, COBOL, SQL and UI validators.
5. Compare each value with what the code you are changing implies. On a conflict, fix consistently with the stricter or enforced value, or stop and name the conflict with both values and locations, in the file and in your final message. Do not choose silently.
6. A rule copied elsewhere has to be fixed there too, or named as left alone. List each site checked.

## 5. Test first

Write a regression test that fails on the current code, following the conventions of the nearest existing tests. Run it and record the failure. Add a case for the common path the fix must not break. If tests cannot run here, say so in the file; do not claim they pass.

## 6. Before every edit

For each file you are about to change:

1. `rules_for(path, start_line, end_line)` on the exact lines; follow `next_call` until it is absent.
2. `entity(entity_id, include:["description","evidence"])` for each rule that touches the change.
3. `read_file(path, start_line, end_line)` to confirm the rule's quote on those lines.

A rule the fix would break stays in force: keep it (the stricter or enforced value), or stop and record the conflict in the file and in your final message. Do not choose silently. `rules_for` also returns rules that only support those lines, so check each. An empty page does not mean no rule applies.

## 7. Fix and verify

Make the smallest change that restores the behavior. Run the regression test and the relevant wider suite. Record the commands you ran and what they printed. CoreStory reads and indexes code; it does not run it, so test results are yours to report.

## 8. Close out

Finish `BUG-NOTES.md`: root cause with `path:start-end`, changed files, the rules you checked before each edit and constraints from other layers (id and `path:start-end`, value), sibling sites changed or left, commands run with results. End with `## Not verified`: rules not read back against source, sites not searched, tests not run, and that CoreStory describes the ingested snapshot, not necessarily the working tree.

Do not call the fix complete or guaranteed.
