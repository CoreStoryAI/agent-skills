---
name: decomposition-sequencing
license: MIT
description: "Break an approved target architecture into dependency-ordered work packages and write them to modernization/04-work-packages.md. Use for migration sequencing, waves, work packages, or an executable modernization backlog."
---

# Decomposition and sequencing

> On hosted CoreStory the tools are prefixed `v3_` (e.g. `v3_rules_for`), take a `project_id` (from `list_projects`), and there is no `status`/`init`/`ingest`: start with `v3_corpus_info`. When following a `next_call`, use the `v3_` name and the same `project_id`.

Output: `modernization/04-work-packages.md`, started early, appended as you go. Phase 4 of `code-modernization`. The engineering lead approves the sequence before work packages are authored.

## 1. Preflight and inputs

Call `status` if available, then `corpus_info` (hosted: `v3_corpus_info` for the chosen project). Proceed only if `status.state` is `snapshot_selected`, the latest ingest has not `failed`, and the `sao:Rule` count is above zero; otherwise relay `status.next_step`. Never call `init` or `ingest` without the user's explicit OK.

Read `modernization/03-target-architecture.md` (must be `approved`, with its ADR filled in) and `modernization/02-rules-inventory.md`. If either is missing or `draft`, stop and name it. Read `01-assessment.md` if present. Exception: under `vibe-modernization` with an existing target there is no `03` file; use the target idioms in an approved `01-assessment.md` instead.

Start the file with the header, `status: draft`, `approver: pending`, `snapshot` from `corpus_info`:

```
---
phase: decomposition-sequencing
status: draft
date: YYYY-MM-DD
snapshot: <id>
approver: pending
---
```

## 2. Part A: units, dependencies, sequence

- Migration units: the smallest sets that can move and be released independently. Use `list_files(prefix)` and `connections(entity_id)` on the programs, modules and tables in scope. Tables or code that force components to move together form a cluster unit.
- Dependencies: hard (must finish first), soft (easier if first), shared data and who owns it, infrastructure prerequisites (gateway, event bus, build pipeline). Cite `path:start-end` for each edge you read with `read_file`; mark inferred edges as inferred.
- Rules: `search(query, kind:"sao:Rule")` per unit, then `rules_for(path, start_line, end_line)` following `next_call`, to list the BR ids each unit must carry. Hits are leads.
- Sequence: order by dependency, then risk, value and team capacity. Name quick wins, parallel lanes, the critical path, and where risk concentrates.

## 3. Gate

Stop after Part A. Ask the engineering lead to approve the sequence and dependency map. Do not author work packages until they approve in this conversation.

## 4. Part B: work packages

After that approval, for each package: scope (included, excluded, temporary integration), BR ids carried, Transform (target patterns, files, tests to write), Coexist (routing, data sync, rollback), Eliminate (what is removed and the check before removal), acceptance criteria. The package id is the slug later phases use (`WP-01`).

Do not create tickets in Jira, Linear or anywhere else unless the user explicitly asks for that external write. Otherwise leave the packages in this file for manual import. Leave `status: draft`; the user approves through `code-modernization`.

End with `## Not verified`: edges inferred rather than read, units not examined, unpaged results, and that results describe the ingested snapshot.

Do not call the plan complete. Do not claim the sequence reduces risk or time. CoreStory does not run code.
