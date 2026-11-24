---
name: using-corestory-with-jira
license: MIT
description: "Work a Jira ticket against the code: read the ticket, find the affected code and rules with CoreStory v3, then resolve it, enrich it with a comment, or draft a new ticket, recorded in JIRA-NOTES.md. Use when given a Jira key or link, asked to triage, estimate, enrich or write up a Jira issue, or to fix a Jira bug or build a Jira story."
---

# CoreStory v3 with Jira

> On hosted CoreStory the tools are prefixed `v3_` (e.g. `v3_rules_for`), take a `project_id` (from `list_projects`), and there is no `status`/`init`/`ingest`: start with `v3_corpus_info`. When following a `next_call`, use the `v3_` name and the same `project_id`.

CoreStory v3 has no Jira integration. Jira comes from a Jira MCP server if one is connected; the code side comes from CoreStory v3. Output: `JIRA-NOTES.md` in the repository root (or the file the user names), created first and appended as you go.

## 1. Preflight

Call `status` if available, then `corpus_info` (hosted: `v3_corpus_info` for the chosen project). Proceed only if `status.state` is `snapshot_selected`, the latest ingest has not `failed`, and the `sao:Rule` count is above zero. Otherwise say CoreStory evidence is unavailable, relay `status.next_step`, and ask whether to continue from source alone. Never call `init` or `ingest` without the user's explicit OK.

Then look in your available tools for a Jira or Atlassian MCP server. If there is none, say so and ask the user to paste the ticket (key, summary, description, acceptance criteria, comments); do not guess ticket content. Setup, if they want it: Atlassian's Rovo MCP server for Jira Cloud (`claude mcp add --transport sse atlassian https://mcp.atlassian.com/v1/sse`) or a community server such as `mcp-atlassian` for Server or Data Center. Tokens never go in repository files.

## 2. Read the ticket

Fetch the ticket (or take the pasted text) and copy summary, description, acceptance criteria, priority, status and links into `JIRA-NOTES.md`. Wrong key, no access or a failed call: say which and stop; do not invent the ticket.

## 3. Route

- Defect to fix: follow `bug-resolver`, with the ticket as the symptom.
- Feature or change: follow `implement-feature`, with the ticket's criteria as the outcome.
- Enrich or triage: step 4.
- Draft a new ticket: step 4, then write the draft in the notes.

## 4. Find the code and the rules

- `search(query)` for the nouns in the ticket; `search(query, kind:"sao:Rule")` with two phrasings per business noun or quantity, then `entity(entity_id, include:["description","evidence"])` and `read_file(path, start_line, end_line)` on the evidence. Hits are leads.
- `connections` on the entities involved for callers, callees and dependencies; `list_files(prefix)` for nearby tests.
- Record: affected files with roles and `path:start-end`, the rules in force (id, values), risks, test surface, and proposed acceptance criteria. Label sizing as an estimate and proposed criteria as proposed. Where the ticket and the code disagree, say which source each claim comes from.

## 5. Jira writes

Draft any comment, new ticket, field change or transition in `JIRA-NOTES.md`. Post it only when the user asks, and say it succeeded only if the Jira tool confirms. On a denied write, a failed transition or a rate limit, keep the draft and report the failure; for transitions, ask the user for the valid next states rather than retrying.

## 6. Close out

End `JIRA-NOTES.md` with `## Not verified`: rules not read back against source, areas not searched, estimates, Jira writes not made, and that CoreStory describes the ingested snapshot, not necessarily the working tree. Do not call the analysis complete.
