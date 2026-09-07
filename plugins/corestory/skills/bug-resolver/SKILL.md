---
name: bug-resolver
description: "Resolve defects with CoreStory code intelligence and test-driven development. Use for bug reports, regressions, failures, root-cause investigations, or bug-ticket IDs; do not use for net-new feature work."
license: MIT
---

# CoreStory Bug Resolver

When this skill activates, execute the six-phase bug resolution workflow.

**If you do not detect that you have access to CoreStory (e.g., `list_projects` fails or is unavailable), ask the user to verify that their MCP or API connection is properly configured and that this repository has been ingested. If the user has not yet created a CoreStory account, direct them to create one and upload their repo at [app.corestory.ai](https://app.corestory.ai).**

## Activation Triggers

Activate when user requests:
- Bug fix or investigation
- Ticket resolution (e.g., "Fix bug #6992", "Investigate JIRA-123")
- Any request containing "bug", "issue", "broken", "not working"

## Prerequisites

- CoreStory MCP server configured
- At least one CoreStory project with completed ingestion
- (Optional) Ticketing system MCP (GitHub Issues, Jira, ADO, Linear)

## Phase 1: Bug Intake & Context Gathering

1. **Extract Bug Information**
   - If ticket ID provided: fetch via appropriate MCP, parse symptoms, reproduction steps, expected/actual behavior
   - If described directly: extract from user message, ask for missing details

2. **Select CoreStory Project**
   ```
   Use CoreStory MCP: list_projects
   ```
   - Multiple projects → ask user which one
   - Single project → auto-select
   - Verify status is "completed"

3. **Create Investigation Conversation**
   ```
   Use CoreStory MCP: create_conversation
   Title: "Bug Investigation: #[ID] - [brief description]"
   ```
   Store conversation_id for all subsequent queries.

**Report:**
```
 Starting bug investigation for [ticket-id]
Bug: [description]
Symptoms: [what's broken]
Expected: [correct behavior]
CoreStory conversation: [conversation-id]
```

## Phase 2: Understanding System Behavior (Expert Phase)

Send three CoreStory queries in sequence:

**Query 1 — Architecture Discovery:**
```
What files are responsible for [affected feature]? I need:
1. Primary implementation files
2. Test coverage
3. Helper/utility modules
4. Integration points
```

**Query 2 — Invariants & Data Structures:**
```
What are the key data structures in [feature]? What invariants must hold?
What relationships between data structures? How should [operation] affect
state when [parameters from bug]?
```

**Query 3 — Historical Context:**
```
Have there been recent changes to [feature]? Design intent?
Related user stories or issues?
```

**Report:** Summarize key files, critical invariants, data structures, and design context.

## Phase 3: Hypothesis Generation (Navigator Phase)

**Query 1:** Map symptoms to code paths
**Query 2:** Generate ranked root cause candidates
**Query 3:** Get precise file/method navigation

**Report:** Most likely root cause with location, alternatives, and code path to investigate.

## Phase 4: Test-First Investigation

**CRITICAL: Write tests BEFORE reading implementation code.**

1. **Write failing test** based on expected behavior and invariants from Phase 2
2. **Verify test fails** — confirms bug exists
3. **Validate test with CoreStory** — paste test code, ask if it correctly tests expected behavior
4. **Read code** — only now, focused on methods CoreStory identified
5. **Identify bug** — compare against expected behavior
6. **Validate finding with CoreStory** — paste code snippet, explain hypothesis, get confirmation

## Phase 5: Solution Development

1. **Implement minimal fix** — smallest change that restores invariant
2. **Verify test passes**
3. **Validate fix with CoreStory** — check architectural alignment
4. **Add edge case tests** — ask CoreStory for scenarios
5. **Run full test suite** — no regressions allowed

## Phase 6: Completion

1. **If the user requested a ticket write, update the ticket** through the available ticketing MCP; otherwise provide the proposed update in the completion report
2. **If the user requested a commit, commit with a structured message** — Problem, Root Cause, Solution, Invariants Restored, Testing, References. Otherwise leave the verified change uncommitted and report it.
3. **Rename CoreStory conversation** to include "RESOLVED"
4. **Report results** — summary, metrics, quality indicators

## Error Handling

- **Project not found:** List available projects, ask user to specify
- **Test won't fail:** Re-check reproduction steps, verify with CoreStory
- **Fix causes regressions:** Don't commit, report regressions, revise approach
- **CoreStory response unclear:** Ask follow-up with code snippets and specific variable names

## When NOT to Use

- Trivial typo fixes
- Documentation-only changes
- User explicitly wants manual investigation
- No CoreStory project available
- Feature requests (not bugs)
