---
name: bug-resolver
license: MIT
description: "Find the root cause of a defect with CoreStory v3 rule evidence, fix it test-first, and write the investigation to BUG-NOTES.md. Use when asked to fix a bug, regression, wrong result, failing behavior, or a bug ticket in a codebase CoreStory has ingested."
---

# Resolve a bug

Output: `BUG-NOTES.md` in the repository root (or the file the user names). Create it first and append as you go. Do not create a ticket, commit, push or publish unless the user asks.

## 1. Preflight

Call `status`, then `corpus_info`. Proceed only if `status.state` is `snapshot_selected`, the latest ingest has not `failed`, and the `sao:Rule` count is above zero. Otherwise say CoreStory evidence is unavailable, relay `status.next_step`, and ask whether to continue from source alone. Never call `init` or `ingest` without the user's explicit OK; `ingest` spends their model-provider money. If `search` says it "could not answer", use `rules_for`, `entity`, `connections` and `read_file`.

## 2. Symptom

Write the symptom, expected behavior, where it shows, and how to reproduce it at the top of `BUG-NOTES.md`. If you can ask for missing details, ask. If you cannot, state your assumptions in the file.

## 3. Investigate

- Rules about the behavior: `search(query, kind:"sao:Rule")`, then `entity(entity_id, include:["description","evidence"])`, then `read_file(path, start_line, end_line)`. Hits are leads; `search` never returns empty.
- Code path: `search(query)` for the symbols and files, `connections` on an entity for callers and callees, `list_files(prefix)` for nearby tests, `read_file` for the lines.
- Hypothesis: write the leading cause and one or two alternatives, each with the `path:start-end` you read.
- Sibling sites: search for the same value or rule in other programs, layers and languages (COBOL, SQL, config, UI). A rule copied elsewhere has to be fixed there too, or named as left alone. List each site checked.

## 4. Test first

Write a regression test that fails on the current code, following the conventions of the nearest existing tests. Run it and record the failure. Add a case for the common path the fix must not break. If tests cannot run here, say so in the file; do not claim they pass.

## 5. Before every edit

For each file you are about to change:

1. `rules_for(path, start_line, end_line)` on the exact lines; follow `next_call` until it is absent.
2. `entity(entity_id, include:["description","evidence"])` for each rule that touches the change.
3. `read_file(path, start_line, end_line)` to confirm the rule's quote on those lines.

A rule the fix would break stays in force: keep it, or stop and record the conflict in the file and in your final message. Do not choose silently. `rules_for` also returns rules that only support those lines, so check each. An empty page does not mean no rule applies.

## 6. Fix and verify

Make the smallest change that restores the behavior. Run the regression test and the relevant wider suite. Record the commands you ran and what they printed. CoreStory reads and indexes code; it does not run it, so test results are yours to report.

## 7. Close out

Finish `BUG-NOTES.md`: root cause with `path:start-end`, changed files, the rules you checked before each edit (id and `path:start-end`), sibling sites changed or left, commands run with results. End with `## Not verified`: rules not read back against source, sites not searched, tests not run, and that CoreStory describes the ingested snapshot, not necessarily the working tree.

Do not call the fix complete or guaranteed.
