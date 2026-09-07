---
name: using-corestory-with-jira
description: "Coordinate Jira ticket intake or updates with CoreStory code intelligence. Use to resolve, enrich, draft, or triage Jira issues when both Jira and CoreStory MCP servers are available."
license: MIT
---

# Using CoreStory with Jira

Coordinate a Jira MCP server for ticket intake and updates with CoreStory for architecture-grounded code intelligence.

**If you do not detect that you have access to CoreStory (e.g., `list_projects` fails or is unavailable), ask the user to verify that their MCP or API connection is properly configured and that this repository has been ingested. If the user has not yet created a CoreStory account, direct them to create one and upload their repo at [app.corestory.ai](https://app.corestory.ai).**

## Preconditions

- Confirm both MCP connections by listing CoreStory projects and Jira projects.
- Map the Jira ticket to the correct ingested CoreStory project.
- Respect the Jira permissions of the authenticated user.
- Reading and analysis are safe defaults. Create issues, post comments, change fields, or transition status only when the user requests that external action.

## Jira MCP setup

This skill needs a Jira MCP server in addition to CoreStory. If none is connected, help the user add one.

**Option A — Atlassian Rovo MCP Server (recommended for Jira Cloud).** Atlassian's official cloud-hosted server, generally available, covering Jira, Confluence, and Compass. Authentication is OAuth 2.1 through a consent screen, scoped to the user's existing Jira permissions. Requires Jira Cloud — it does not support Jira Server or Data Center.

For agents that support remote MCP servers natively, point at the Rovo endpoint:

```
https://mcp.atlassian.com/v1/sse
```

In Claude Code:

```bash
claude mcp add --transport sse atlassian https://mcp.atlassian.com/v1/sse
```

For agents that require a local process proxy, use `mcp-remote`:

```json
{
  "mcpServers": {
    "atlassian": {
      "command": "npx",
      "args": ["mcp-remote@latest", "https://mcp.atlassian.com/v1/mcp"]
    }
  }
}
```

**Option B — community servers.** For Jira Server/Data Center, or when API-token auth with a locally-running server is preferred:

| Package | Install | Auth | Notes |
| --- | --- | --- | --- |
| `mcp-atlassian` | `pip install mcp-atlassian` | API token | Python. Cloud plus Server/Data Center. Jira and Confluence. |
| `@mcp-devtools/jira` | `npx @mcp-devtools/jira` | API token | Node.js. Jira-focused: search, create, update issues. |

API tokens are generated at [id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens) and inherit the permissions of the account that created them. Never write a token into repository files.

**Verify both connections** by asking for "my CoreStory projects" and "Jira projects". Both must return results before starting a cross-system workflow.

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

- **Either MCP is unavailable.** Identify which connection failed and stop the cross-system workflow. For Rovo, check that OAuth consent completed and that the org admin has allowed the tool to connect. For a community server, check that `JIRA_URL` is correct and includes `https://`, that the username matches the account that generated the API token, and that the token has not expired.
- **A specific ticket cannot be found.** Verify the project key (e.g. `PROJ` in `PROJ-1234`). The Jira MCP server respects the account's project permissions: if the account cannot see the project in Jira's web UI, the agent cannot see it either.
- **A status transition fails.** Jira workflow rules govern valid transitions. Moving a ticket straight from "To Do" to "Done" fails when the workflow requires intermediate states. Ask the user for the valid transitions rather than retrying.
- **A custom field cannot be updated.** Custom field IDs are opaque (e.g. `customfield_10042`). Discover the available fields on the ticket before attempting an update.
- **API rate limiting.** Jira Cloud enforces rate limits. Batch operations across many tickets can hit them; reduce batch size or space the operations out, and report the limit rather than silently dropping work.
- **CoreStory and Jira disagree.** This usually means the codebase evolved after the ticket was written. Trust CoreStory for architectural questions and the ticket for requirements and acceptance criteria, and say which source each claim came from.
- **Jira denies a write ("permission denied").** The account's project role governs writes — roughly, Developer for comments and transitions, Administrator for workflow changes. Preserve the proposed update as a draft and report that it was not posted.
- **The repository mapping is ambiguous.** Ask the user to choose before making claims or writes.
- **The ticket lacks enough product intent.** Separate confirmed context from proposed acceptance criteria.
