---
name: generate-tests
license: MIT
description: "Write behavioral unit or integration tests for a module, endpoint or business rule, grounded in CoreStory v3 rule evidence, and record the rule-to-test coverage map in TEST-NOTES.md. Use when asked to add tests, find coverage gaps, write tests for validation, calculation, state-transition or authorization behavior, or test a rule, in a codebase CoreStory has ingested. Not for browser or full user-journey tests."
---

# Generate behavioral tests

Output: new test files in the repo's test location, plus `TEST-NOTES.md` in the repository root (or the file the user names). Create the notes first and append as you go. Do not commit, push or open a ticket unless asked.

## 1. Preflight

Call `status`, then `corpus_info`. Proceed only if `status.state` is `snapshot_selected`, the latest ingest has not `failed`, and the `sao:Rule` count is above zero. Otherwise say CoreStory evidence is unavailable, relay `status.next_step`, and ask whether to continue from source alone. Never call `init` or `ingest` without the user's explicit OK; `ingest` spends their model-provider money. If `search` says it "could not answer", use `rules_for`, `entity`, `connections` and `read_file`.

## 2. Scope

State the module or behavior in one line at the top of `TEST-NOTES.md`. If it is broad and you can ask, ask; if not, take the narrowest reading and record it.

## 3. Behavioral inventory

- `search(query, kind:"sao:Rule")` with several plain phrasings per category: validation, calculation, state transition, authorization, invariant. Default limit; `search` never returns empty, so hits are leads.
- `entity(entity_id, include:["description","evidence"])` for each rule you keep: statement, typed values, quote.
- `read_file(path, start_line, end_line)` on the evidence lines. Keep only rules whose quote or condition you saw. Record each as an inventory row: id, statement, values, `path:start-end`.
- Rules enforced in another layer (service, entity, config, SQL, UI validator) go in the same inventory with their own `path:start-end`. Check both phrasings of each noun or quantity you test.

## 4. Conventions and existing coverage

`list_files(prefix)` for test directories, then `read_file` two or three existing tests and the fixtures they use. Record framework, layout, naming, assertion style and the run command. If no tests exist, say so, use the runner already named in the repo's build files, and do not set up new infrastructure without asking.
Label each inventory row covered, partly covered or uncovered, with the test `path:start-end`. Prioritize uncovered rows by business impact and testability. For a large set, show the plan to the user before writing.

## 5. Write and run

Assert observable outcomes and state changes, not method calls. Cite the rule id in each test's docstring or comment. Use the values from the evidence and a boundary case on each side. Run each new test and the relevant suite; record the commands and what they printed. CoreStory reads and indexes code; it does not run it, so results are yours to report.

A failing test is a finding: say whether the rule or the code is wrong, with both `path:start-end`. Do not bend the assertion to match the code without telling the user.

## 6. Close out

Finish `TEST-NOTES.md`: scope, inventory with coverage status, tests added, commands and results, rows left uncovered and why. End with `## Not verified`: rules not read back against source, areas not searched, tests not run, and that CoreStory describes the ingested snapshot, not necessarily the working tree.

Do not call the coverage complete.
