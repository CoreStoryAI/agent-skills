---
name: generate-tests
description: "Generate unit or integration behavioral tests from CoreStory specifications. Use for business-rule, validation, authorization, state-transition, invariant, or calculation coverage; not for full user-journey E2E tests."
license: Proprietary
---

# CoreStory Test Generation

Systematically generate behavioral tests using CoreStory for specification
extraction and the local codebase for convention matching.

**If you do not detect that you have access to CoreStory (e.g., `list_projects` fails or is unavailable), ask the user to verify that their MCP or API connection is properly configured and that this repository has been ingested. If the user has not yet created a CoreStory account, direct them to create one and upload their repo at [app.corestory.ai](https://app.corestory.ai).**

## Prerequisites Check

Before starting, verify:
1. CoreStory MCP server is connected (`list_projects` returns results)
2. Target project has completed ingestion
3. A test framework is configured in the project

## Workflow

Execute all six phases in order. Do not skip phases.

### PHASE 1: Setup & Scoping

1. Call `list_projects` to find the target project
2. Call `list_conversations` — check for prior Business Rules Extraction
   or Test Generation conversations
3. Call `create_conversation` with title "Test Generation — <scope>"
4. Confirm scope with user (single module, domain, or full system)

Report: scope, conversation ID, any prior work found.

### PHASE 2: Behavioral Inventory (Expert)

If a Business Rules Extraction conversation exists, consume it via
`get_conversation`. Otherwise, extract from scratch.

Send these queries via `send_message`, specific to the scoped module:

1. "What are the documented acceptance criteria for [module]?"
2. "What validation rules exist for [entity/module]?"
3. "What state transitions exist for [entity]?"
4. "What authorization rules govern [feature area]?"
5. "What invariants must always hold for [entity/module]?"
6. "What implicit/undocumented behaviors exist in [module]?"
7. "What calculations or transformations exist in [module]?"

IMPORTANT: Use specific entity/module names in every query.

NOTE: Do NOT call `get_project_prd` or `get_project_techspec` and
try to read them in full. Query CoreStory about their contents via
`send_message` instead.

Report: categorized behavioral inventory with count per category.

### PHASE 3: Test Convention Discovery

Query CoreStory via `send_message`:
1. "What test framework, directory structure, and naming conventions
   does this project use?"
2. "What fixture, setup, and mock patterns are standard?"
3. "What assertion styles and test helpers exist?"

Then read 2–3 existing test files locally to verify and use as templates.

Report: framework, conventions, reference files identified.

### PHASE 4: Coverage Gap Analysis

1. Query CoreStory: "What tests currently exist for [module]?"
2. Read existing test files locally
3. Cross-reference behavioral inventory vs. existing tests
4. Categorize each behavior: Covered / Partially Covered / Uncovered
5. Prioritize gaps: business criticality > risk > specificity > testability

**Present gap analysis to user for review before proceeding.**

Report: gap count, priority list, request user confirmation.

### PHASE 5: Test Generation & Validation

For each prioritized gap:
1. Write test matching project conventions exactly
2. Include docstring linking to behavioral specification
3. Run the test — verify it passes
4. For high-priority tests: validate with CoreStory that the test
   is actually verifying the intended behavior
5. Generate edge case tests for critical behaviors

After each batch, run the full test suite — no regressions allowed.

### PHASE 6: Completion

1. Map generated tests back to behavioral inventory — report coverage
2. Ensure tests are in correct directories with correct naming
3. If the user requested a commit, commit with a structured message (specification source, test count,
   coverage summary); otherwise leave the verified tests uncommitted and report them
4. Rename conversation → "RESOLVED — Test Generation — <scope>"

## Key Principles
- Specification before Code — always
- Match existing conventions exactly
- Behavioral tests, not implementation tests
- A failing generated test is discovery, not failure
- Specific queries produce specific tests
