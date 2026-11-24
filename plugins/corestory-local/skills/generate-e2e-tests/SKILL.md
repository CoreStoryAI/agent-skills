---
name: generate-e2e-tests
license: MIT
description: "Write end-to-end tests for a critical user journey, API flow or cross-service path, grounded in CoreStory v3 rule and code-path evidence, and record the journey inventory in E2E-NOTES.md. Use when asked for end-to-end, journey, browser, API-to-database or workflow tests in a codebase CoreStory has ingested. For rule-level unit or integration tests use generate-tests."
---

# Generate end-to-end tests

> On hosted CoreStory the tools are prefixed `v3_` (e.g. `v3_rules_for`), take a `project_id` (from `list_projects`), and there is no `status`/`init`/`ingest`: start with `v3_corpus_info`. When following a `next_call`, use the `v3_` name and the same `project_id`.

Output: new E2E test files in the repo's E2E location, plus `E2E-NOTES.md` in the repository root (or the file the user names). Create the notes first and append as you go. Do not commit, push or open a ticket unless asked.

## 1. Preflight

Call `status` if available, then `corpus_info` (hosted: `v3_corpus_info` for the chosen project). Proceed only if `status.state` is `snapshot_selected`, the latest ingest has not `failed`, and the `sao:Rule` count is above zero. Otherwise say CoreStory evidence is unavailable, relay `status.next_step`, and ask whether to continue from source alone. Never call `init` or `ingest` without the user's explicit OK; `ingest` spends their model-provider money. If `search` says it "could not answer", use `rules_for`, `entity`, `connections` and `read_file`.

## 2. Scope

Name one journey (or a short cluster) at the top of `E2E-NOTES.md`. If you can ask, ask; if not, take the narrowest reading and record it.

## 3. Journey trace

CoreStory has no journey or acceptance-criteria store. You build the journey from code and rules.
- Entry points: `search(query)` for the route, handler, screen or command; `read_file(path, start_line, end_line)` to confirm.
- Path: `connections` on each entity for callers and callees, across layers; `read_file` the hops. Write the steps as `step: path:start-end`.
- Rules on the path: `search(query, kind:"sao:Rule")` with two phrasings per noun the journey touches, then `entity(entity_id, include:["description","evidence"])` and `read_file` on the evidence. Each verified rule becomes an assertion with its values; hits are leads, not proof.
- Preconditions, seed data and the failure branches (rejections, limits, error codes) come from the same reads.

## 4. Conventions and environment

`list_files(prefix)` for existing E2E tests, then read two or three, with their config, fixtures and auth setup. Record framework, selectors or client, data isolation and the run command. Confirm a test environment exists (app startup, database, test client). If there is no E2E framework or environment, say so, propose the smallest fit in the repo's own stack (for example an HTTP-level test through the real app and database), and ask before adding dependencies.

## 5. Write and run

Happy path first, then the failure branches that the verified rules define. Wait on conditions, not fixed delays; isolate test data. If you can run the tests, run each three times and record results; if you cannot, say so. CoreStory does not run or test code; results are yours to report. A failing test is a finding: say whether the rule or the code is wrong, with both `path:start-end`; do not bend the assertion silently.

## 6. Close out

Finish `E2E-NOTES.md`: journey steps with `path:start-end`, rules asserted (id, values), tests added, commands and results, branches not covered. End with `## Not verified`: hops or rules not read back, layers not searched, tests not run, and that CoreStory describes the ingested snapshot, not necessarily the working tree.

Do not call the coverage complete.
