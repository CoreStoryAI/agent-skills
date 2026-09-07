---
name: implement-feature
description: "Implement features and enhancements with CoreStory code intelligence and test-driven development. Use for feature tickets or requested product changes; do not use for defect investigation or bug fixes."
license: MIT
---

# CoreStory Feature Implementation

Systematically implement feature tickets using CoreStory for architectural
guidance and test-driven development for quality.

**If you do not detect that you have access to CoreStory (e.g., `list_projects` fails or is unavailable), ask the user to verify that their MCP or API connection is properly configured and that this repository has been ingested. If the user has not yet created a CoreStory account, direct them to create one and upload their repo at [app.corestory.ai](https://app.corestory.ai).**

## Prerequisites Check

Before starting, verify:
1. CoreStory MCP server is connected (`list_projects` returns results)
2. Target project has completed ingestion
3. Ticket details are available (via ticketing MCP or user-provided)

## Workflow

Execute all six phases in order. Do not skip phases.

### PHASE 1: Ticket Intake

1. If user provided a ticket ID: fetch it via the appropriate ticketing MCP.
   If user described the feature directly: extract description and ask for
   acceptance criteria if not provided.
2. Select CoreStory project:
   - Call `list_projects`
   - If multiple: ask user which one
   - If one: auto-select
   - Verify project ingestion status is "completed"
3. Create implementation conversation:
   - Call `create_conversation` with title "Ticket Implementation: #[ID] - [description]"
   - Store conversation_id for all subsequent queries

Report to user: ticket summary, acceptance criteria, conversation ID.

### PHASE 2: Expert Phase (Architecture Understanding)

Send these queries to CoreStory via `send_message`. After each, summarize
key findings to user.

**Query 1 — Architecture discovery:**
"What files are responsible for [feature area]? I need: primary implementation
files, existing test patterns, reusable helper modules, integration points."

**Query 2 — Design patterns and conventions:**
"What architectural patterns are used for [feature type]? How are similar
features structured? What naming conventions apply? What invariants must
I maintain?"

**Query 3 — Historical context:**
"Have similar features been implemented recently? What was the design intent?
Are there related PRs or tickets?"

Parse responses for: core files, reference implementations, naming conventions,
invariants (CRITICAL — these must not be violated), and known gotchas.

### PHASE 3: Navigator Phase (Implementation Planning)

**Query 1 — Extension points:**
"Where should I implement [feature]? What files to create, what files to
modify? Walk me through step by step."

**Query 2 — Data structures:**
"What data structures should I use? What models/schemas are involved?
What relationships and dependencies exist?"

**Query 3 — Reference implementations:**
"What existing features are most similar? Can I reuse code or patterns?"

Output to user: files to create, files to modify, data structures, reference
pattern to follow.

### PHASE 4: TDD Implementation

**CRITICAL: Tests come BEFORE implementation code.**

1. Write acceptance tests from Phase 1 criteria, following Phase 2 patterns
   and Phase 3 data structures. Use naming pattern:
   `test_[feature]_[scenario]_[expected]`
2. Write unit tests for individual components.
3. Verify all tests FAIL. If they pass, the feature may already exist —
   check with CoreStory.
4. Validate tests with CoreStory: paste test code and ask if they correctly
   validate the acceptance criteria and follow established testing patterns.
5. Implement the feature following patterns from Phase 2.
6. Verify all tests PASS.
7. Validate implementation with CoreStory: paste code structure and ask if
   it aligns with architecture and could have unintended side effects.

### PHASE 5: Feature Completion

1. Ask CoreStory for edge cases: "What edge cases should I test? What
   scenarios might break in production?"
2. Add edge case tests (empty state, large data, concurrent access,
   invalid input, permission boundaries).
3. Run FULL test suite — all tests must pass, no regressions.
4. If feature has performance requirements: add performance tests.
5. If feature handles auth or sensitive data: add security tests.

### PHASE 6: Completion

1. If the user requested a ticket write and a ticketing MCP is available, update the ticket with the implementation summary; otherwise provide the proposed update without posting it.
2. If the user requested a commit, commit with a detailed message; otherwise leave the verified change uncommitted:
   - Format: "Feat: [description] (#[ticket-id])"
   - Include: feature summary, implementation details, architecture
     alignment notes, test count and categories, references
3. Rename CoreStory conversation:
   "Ticket Implementation: #[ID] - COMPLETED - [description]"
4. Report to user: summary, commit status, test results, and quality metrics.

## When NOT to Use This Skill

- Trivial changes (typos, formatting)
- Documentation-only changes
- Bug fixes (use the `bug-resolver` skill instead)
- No CoreStory project available
- User explicitly wants to implement manually
