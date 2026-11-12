---
name: generate-tests
license: MIT
description: "Generate behavioral unit or integration tests using local CoreStory evidence. Use for validation, authorization, state-transition, invariant, or calculation coverage, not full end-to-end journeys."
---

# Generate behavioral tests

Confirm the local code graph with `corpus_info`.
Set a specific module or behavior scope before generating tests.
Search for the behavior, invariants, existing tests, test helpers, and comparable implementations.
Read several existing test files and the implementation source to verify conventions and actual behavior.

Build a behavioral inventory from source-backed rules.
Map each behavior to existing coverage and label it covered, partly covered, or uncovered.
Prioritize gaps by criticality, risk, and testability.
Present the proposed test set before making changes when the scope is substantial.

Write tests that prove observable behavior rather than implementation details.
Follow local fixture, naming, and assertion conventions.
Run each new test and the relevant suite.
A failing test is useful evidence; distinguish a discovered defect from an incorrect test assumption.

Report the new coverage, evidence locations, tests added, commands run, and gaps left intentionally uncovered.
Do not create a ticket, commit, or publish a change unless the user asks.
