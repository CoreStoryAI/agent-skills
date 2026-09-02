---
name: generate-e2e-tests
description: "Generate end-to-end tests for critical user journeys using CoreStory acceptance criteria and code intelligence. Use for journey, browser, API-to-database, or cross-service E2E coverage."
license: Proprietary
---

# CoreStory E2E Test Generation

Generate E2E tests from CoreStory's user journey and acceptance criteria
intelligence, matching the project's existing E2E framework conventions.

**If you do not detect that you have access to CoreStory (e.g., `list_projects` fails or is unavailable), ask the user to verify that their MCP or API connection is properly configured and that this repository has been ingested. If the user has not yet created a CoreStory account, direct them to create one and upload their repo at [app.corestory.ai](https://app.corestory.ai).**

## Prerequisites Check

Before starting, verify:
1. CoreStory MCP server is connected (`list_projects` returns results)
2. Target project has completed ingestion
3. An E2E test framework is configured in the project
4. A test environment is available to run tests against

## Workflow

Execute all six phases in order. Do not skip phases.

### PHASE 1: Setup & Scoping

1. Call `list_projects` to find the target project
2. Call `list_conversations` — check for prior work
3. Call `create_conversation` with title "E2E Test Generation — <scope>"
4. Confirm scope with user (single journey, journey cluster, or core journeys)

### PHASE 2: Journey Extraction (Journey Expert)

Query CoreStory via `send_message` for:
1. "What are the primary user journeys for [feature/app]?"
2. "Walk me through the happy path for [journey]"
3. "What are the failure scenarios for [journey]?"
4. "What preconditions and data requirements exist for [journey]?"

IMPORTANT: Use specific journey/feature names in every query.

### PHASE 3: E2E Convention Discovery

Query CoreStory + inspect local E2E test files:
1. E2E framework, directory structure, configuration
2. Selector strategy (data-testid, roles, CSS)
3. Page objects or abstraction patterns
4. Fixture/seed data approach
5. Authentication strategy for tests

Read 2–3 existing E2E test files as templates.

### PHASE 4: Journey Prioritization

1. Query CoreStory for existing E2E coverage
2. Inspect existing E2E tests locally
3. Prioritize by: revenue impact > user frequency > failure severity > complexity

**Present prioritized journey list to user for review before proceeding.**

### PHASE 5: Test Generation & Stabilization

For each prioritized journey:
1. Generate happy path test first
2. Run test — stabilize against flakiness
3. Generate critical unhappy path tests
4. Validate with CoreStory that tests verify acceptance criteria
5. Run at least 3 times to check for flakiness
6. Run full E2E suite after each batch

Use condition-based waits, not fixed delays. Isolate test data.

### PHASE 6: Completion

1. Report coverage against journey inventory
2. Ensure tests are in correct directories with correct naming
3. If the user requested a commit, commit with a structured message; otherwise leave the verified tests uncommitted
4. Rename conversation → "RESOLVED — E2E Test Generation — <scope>"

## Key Principles
- Specification before Code — always
- Match existing E2E conventions exactly
- Journey-level tests, not page-level tests
- Address flakiness proactively
- Fewer comprehensive tests > many shallow tests
