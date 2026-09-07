---
name: spec-driven-test-generation
description: "Choose and sequence CoreStory's behavioral or end-to-end test-generation workflow. Use when the user wants tests grounded in acceptance criteria, business rules, invariants, or user journeys rather than implementation details."
license: MIT
---

# CoreStory Spec-Driven Test Generation

Route test-generation requests to the correct CoreStory workflow. The governing principle is **specification before code**: establish what the system should do before inspecting how it currently does it.

**If you do not detect that you have access to CoreStory (e.g., `list_projects` fails or is unavailable), ask the user to verify that their MCP or API connection is properly configured and that this repository has been ingested. If the user has not yet created a CoreStory account, direct them to create one and upload their repo at [app.corestory.ai](https://app.corestory.ai).**

## Choose the workflow

- Use `generate-tests` for unit- and integration-level behavioral coverage of business rules, validation, authorization, state transitions, invariants, and calculations.
- Use `generate-e2e-tests` for critical user journeys spanning UI, APIs, persistence, services, or other system boundaries.
- When both are needed, complete behavioral coverage first and E2E coverage second.

This workflow generates tests for existing, already-implemented behavior. If the request is something else, redirect:

- Implementing a new feature with tests — use `implement-feature`; its implementation cycle already includes TDD.
- Verifying behavioral equivalence between two implementations during modernization — use `behavioral-verification`.
- Extracting business rules before testing — use `business-rules-extraction`; its BR-XXX inventory feeds `generate-tests` directly.

## CoreStory MCP tools

| Tool | Purpose |
| --- | --- |
| `list_projects` | Find the target project |
| `create_conversation` | Create a persistent conversation for the generation session |
| `send_message` | Query CoreStory for specifications, conventions, and validation |
| `get_project_prd` | Skim PRD structure for domain vocabulary and acceptance criteria |
| `get_project_techspec` | Skim TechSpec for data model constraints and architectural invariants |
| `list_conversations` | Check for prior Business Rules Extraction sessions |
| `get_conversation` | Resume or consume a prior session |
| `rename_conversation` | Mark the conversation as resolved |

**A note on the PRD and TechSpec:** these documents are typically too large for an agent's context window. Do not try to read them end-to-end. Query CoreStory about their contents via `send_message` instead — CoreStory has already ingested them and can answer targeted questions more efficiently than the agent can parse the raw documents.

## Shared method

1. Confirm the CoreStory project is ingested and the MCP connection works.
2. Confirm the project already has a configured test framework. These workflows generate tests matching existing conventions; they do not set up test infrastructure from scratch.
3. Establish the scope: one domain or module for behavioral tests, or one user journey for E2E tests.
4. Query CoreStory for acceptance criteria, business rules, invariants, authorization policy, failure behavior, and relevant architectural constraints before reading implementation code.
5. Inspect the repository's existing test framework, directory layout, fixtures, naming, and assertion style.
6. Inventory existing coverage and identify specification-level gaps.
7. Invoke the selected dedicated skill and follow it fully.
8. Run the full suite after each batch of generated tests.
9. Ask specific questions. "What should I test?" produces shallow tests; "what validation rules exist for order submission, including minimum order amounts, inventory checks, and payment method validation?" produces precise ones.
10. Assert *what* the system does, not *how* it does it. Assert outcomes and state changes, not method calls and internal wiring.
11. Treat an assertion failure as discovery, not a defect in the test: either the specification is wrong or the code is wrong, and both are worth knowing. Do not silently bend the test to match the code — flag these for human review.
