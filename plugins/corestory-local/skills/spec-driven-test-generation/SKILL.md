---
name: spec-driven-test-generation
license: MIT
description: "Decide whether a testing request needs rule-level behavioral tests or end-to-end journey tests, then run the right CoreStory v3 skill. Use when asked to write tests from the business rules, acceptance criteria or specification, test what the system should do rather than how it is built, or when unsure whether to write unit, integration or end-to-end tests."
---

# Choose the test-generation workflow

Principle: establish what the system must do (verified rules, the user's acceptance criteria) before reading how the code does it, and assert outcomes, not wiring.

## Route

- Validation, calculation, authorization, state transitions, invariants, one module or endpoint: use `generate-tests`.
- A user journey or flow across UI, API, persistence or services: use `generate-e2e-tests`.
- Both: `generate-tests` first, then `generate-e2e-tests` for the journeys that tie the tested rules together.

Redirect other requests:
- A new feature with tests: `implement-feature` (test-first is in its cycle).
- Extracting the rules without tests: `business-rules-extraction`.
- A defect: `bug-resolver`.
- Equivalence of a rewrite against the original: not this skill; compare outputs of both implementations on shared cases.

## Shared method

1. Preflight is each skill's step 1: `status`, then `corpus_info`. Stop and relay `status.next_step` if the snapshot is not ready. Never call `init` or `ingest` without the user's OK.
2. Confirm the repo already has a test framework; these skills match existing conventions and do not set up infrastructure unasked.
3. Fix the scope to one module or one journey. Specific nouns find specific rules: use `search(query, kind:"sao:Rule")` with the concrete entities and quantities, not "what should I test".
4. Hand off to the chosen skill and follow it. Its notes file (`TEST-NOTES.md` or `E2E-NOTES.md`) is the deliverable.
5. Run the suite after each batch. CoreStory reads and indexes code; it does not run it, so test results are yours to report.
6. A failing generated test is a finding: either the rule read from the graph is wrong or the code is. Show both `path:start-end` to the user; do not bend the test silently.

Do not call the generated coverage complete.
