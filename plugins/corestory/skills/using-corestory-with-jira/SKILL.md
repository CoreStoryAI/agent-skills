---
name: using-corestory-with-jira
description: "Coordinate Jira ticket intake or updates with CoreStory code intelligence. Use to resolve, enrich, draft, or triage Jira issues when both Jira and CoreStory MCP servers are available."
license: Proprietary
---

# Using CoreStory with Jira

Coordinate a Jira MCP server for ticket intake and updates with CoreStory for architecture-grounded code intelligence.

## Preconditions

- Confirm both MCP connections by listing CoreStory projects and Jira projects.
- Map the Jira ticket to the correct ingested CoreStory project.
- Respect the Jira permissions of the authenticated user.
- Reading and analysis are safe defaults. Create issues, post comments, change fields, or transition status only when the user requests that external action.

## Route the request

- **Resolve:** Fetch the ticket, classify it as a bug or feature, then use `bug-resolver` or `implement-feature` for the code workflow.
- **Enrich:** Query CoreStory for affected files, patterns, dependencies, risks, tests, and suggested acceptance criteria; draft or post a structured Jira comment as requested.
- **Draft:** Use CoreStory to identify an actionable issue, then prepare or create a Jira ticket with evidence, scope, acceptance criteria, and validation guidance.
- **Triage:** Assess likely files, dependencies, risk, test surface, and relative complexity. Label estimates as estimates rather than facts.

## Resolve workflow

1. Read the ticket's summary, description, acceptance criteria, priority, comments, links, and current status.
2. Select the CoreStory project and create a ticket-specific conversation.
3. Query CoreStory for architecture, relevant files, dependencies, similar implementations, and constraints.
4. Follow the dedicated bug or feature skill, including its tests and human gates.
5. Prepare a Jira update containing root cause or implementation summary, files changed, tests run, results, and remaining risks.
6. Post the update or transition status only if the user requested it. Never imply a Jira write succeeded unless the Jira tool confirms it.

## Enrichment output

Include affected files with roles, recommended existing pattern, dependencies, risks, suggested acceptance criteria, test guidance, and estimated complexity with rationale.

## Failure handling

- If either MCP is unavailable, identify which connection failed and stop the cross-system workflow.
- If the repository mapping is ambiguous, ask the user to choose before making claims or writes.
- If the ticket lacks enough product intent, separate confirmed context from proposed acceptance criteria.
- If Jira denies a write, preserve the proposed update as a draft and report that it was not posted.
