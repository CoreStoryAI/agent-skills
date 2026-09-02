---
name: spec-driven-test-generation
description: "Choose and sequence CoreStory's behavioral or end-to-end test-generation workflow. Use when the user wants tests grounded in acceptance criteria, business rules, invariants, or user journeys rather than implementation details."
license: Proprietary
---

# CoreStory Spec-Driven Test Generation

Route test-generation requests to the correct CoreStory workflow. The governing principle is **specification before code**: establish what the system should do before inspecting how it currently does it.

## Choose the workflow

- Use `generate-tests` for unit- and integration-level behavioral coverage of business rules, validation, authorization, state transitions, invariants, and calculations.
- Use `generate-e2e-tests` for critical user journeys spanning UI, APIs, persistence, services, or other system boundaries.
- When both are needed, complete behavioral coverage first and E2E coverage second.

Do not use this router to implement a new feature, fix a bug, or compare two implementations during modernization. Use `implement-feature`, `bug-resolver`, or `behavioral-verification` respectively.

## Shared method

1. Confirm the CoreStory project is ingested and the MCP connection works.
2. Establish the scope: one domain/module for behavioral tests or one user journey for E2E tests.
3. Query CoreStory for acceptance criteria, business rules, invariants, authorization policy, failure behavior, and relevant architectural constraints before reading implementation code.
4. Inspect the repository's existing test framework, directory layout, fixtures, naming, and assertion style.
5. Inventory existing coverage and identify specification-level gaps.
6. Invoke the selected dedicated skill and follow it fully.
7. Run the smallest relevant tests first, then the broader suite warranted by the change.
8. Treat an assertion failure as a specification-versus-implementation finding; do not silently bend the test to match the code.

## Output

Report the specifications covered, tests added or changed, commands and results, uncovered behaviors, and any discrepancy requiring human review.
