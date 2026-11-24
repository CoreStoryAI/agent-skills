---
name: implement-feature
license: MIT
description: "Implement a feature, endpoint, field, or change to existing behavior with CoreStory v3 rule evidence and test-first development, and write the design and assumptions to FEATURE-NOTES.md. Use when asked to add, build or change something in a codebase CoreStory has ingested, or to work a feature ticket or change request."
---

# Implement a feature

> On hosted CoreStory the tools are prefixed `v3_` (e.g. `v3_rules_for`), take a `project_id` (from `list_projects`), and there is no `status`/`init`/`ingest`: start with `v3_corpus_info`. When following a `next_call`, use the `v3_` name and the same `project_id`.

Output: `FEATURE-NOTES.md` in the repository root (or the file the user names). Create it first and append as you go. Do not create a ticket, commit, push or publish unless the user asks.

## 1. Preflight

Call `status` if available, then `corpus_info` (hosted: `v3_corpus_info` for the chosen project). Proceed only if `status.state` is `snapshot_selected`, the latest ingest has not `failed`, and the `sao:Rule` count is above zero. Otherwise say CoreStory evidence is unavailable, relay `status.next_step`, and ask whether to continue from source alone. Never call `init` or `ingest` without the user's explicit OK; `ingest` spends their model-provider money. If `search` says it "could not answer", use `rules_for`, `entity`, `connections` and `read_file`.

## 2. Outcome

Write the requested outcome and acceptance criteria at the top of `FEATURE-NOTES.md`. If you can ask about missing criteria, ask. If you cannot, take the narrowest reasonable reading and list each assumption.

## 3. Cross-layer concept sweep (required before any edit)

A ticket names what to build, not every rule the result must respect, and a rule for a value often lives in a different layer than the file you will change.

1. List the business nouns and quantities the ticket touches (amounts, counts, thresholds, dates, statuses) at the top of the notes file.
2. For each, run `search(query, kind:"sao:Rule")` with at least two plain-language phrasings of the concept, default limit. Do not paste the ticket text.
3. Open with `entity(entity_id, include:["description","evidence"])` every hit whose file is not one you plan to edit and whose statement constrains the same noun or quantity, then `read_file` the evidence lines. Hits are leads.
4. Record each as `constraint from another layer: path:start-end, value`. Look across services, entities, config, COBOL, SQL and UI validators.
5. Compare each value with what the ticket or the code you are changing implies. On a conflict, implement consistently with the stricter or enforced value, or stop and name the conflict with both values and locations, in the file and in your final message. Do not choose silently.
6. If the feature reports a decision other code makes (is this allowed, what does it cost, when is it due), find that code with `search` and `connections` and reuse its function. Do not copy its number into a second place.

## 4. Pattern and boundary

Find the closest existing feature: `search(query)`, `list_files(prefix)`, `connections`, `read_file`. Write the implementation boundary: files to change or add, the pattern copied, the rules kept, the tests to write.

## 5. Tests first

Write acceptance tests from the criteria, plus one test for each constraint from step 3 that bears on the output. Run them and record that they fail for the missing behavior. If tests cannot run here, say so in the file.

## 6. Before every edit

For each file you are about to change:

1. `rules_for(path, start_line, end_line)` on the exact lines; follow `next_call` until it is absent.
2. `entity(entity_id, include:["description","evidence"])` for each rule that touches the change.
3. `read_file(path, start_line, end_line)` to confirm the quote on those lines.

A rule that the feature would violate stays in force: honor it (the stricter or enforced value), or stop and record the conflict in the file and in your final message. Do not choose silently. `rules_for` also returns rules that only support those lines, so check each.

## 7. Implement and verify

Make the smallest change that meets the criteria and follows local conventions. Run the new tests and the relevant wider suite. Record the commands and what they printed. CoreStory reads and indexes code; it does not run it, so test results are yours to report.

## 8. Close out

Finish `FEATURE-NOTES.md`: behavior delivered, rules honored and constraints from other layers (id and `path:start-end`, value), assumptions, changed files, commands run with results. End with `## Not verified`: rules not read back against source, layers not searched, tests not run, and that CoreStory describes the ingested snapshot, not necessarily the working tree.

Do not call the feature complete or guaranteed.
