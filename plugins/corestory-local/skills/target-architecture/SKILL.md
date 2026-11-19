---
name: target-architecture
license: MIT
description: "Lay out modernization strategy options (the seven Rs) and a target architecture with trade-offs, then record the human's decision as an ADR in modernization/03-target-architecture.md. Use after the assessment and rules inventory are approved, for strategy selection, target-state design, or an architecture decision record."
---

# Target architecture and strategy

Output: `modernization/03-target-architecture.md`, started at the top of the work and appended as you go. Phase 3 of `code-modernization`. The architect or tech lead decides; you do not.

## 1. Preflight and inputs

Call `status`, then `corpus_info`. Proceed only if `status.state` is `snapshot_selected`, the latest ingest has not `failed`, and the `sao:Rule` count is above zero; otherwise relay `status.next_step`. Never call `init` or `ingest` without the user's explicit OK.

Read `modernization/01-assessment.md` and `modernization/02-rules-inventory.md`. Each must have `status: approved` in its header. If one is missing or still `draft`, stop and name it. Summarize their blockers, coupling hotspots, shared data and rules at the top of your file.

Start the file with this header, `status: draft`, `approver: pending`, `snapshot` from `corpus_info`:

```
---
phase: target-architecture
status: draft
date: YYYY-MM-DD
snapshot: <id>
approver: pending
---
```

## 2. Explore the option space

Scope is the system or components the user names; if broad and you can ask, ask.

- Structure and seams: `list_files(prefix)`, then `connections(entity_id)` on the main programs, modules and tables, to see what calls and shares what.
- Constraints on moving a component: `search(query, kind:"sao:Rule")` for the concept, then `entity(entity_id, include:["description","evidence"])`. Rules that depend on shared data, ordering or batch timing limit the options.
- `read_file(path, start_line, end_line)` on the lines you cite. Hits are leads; cite only what you read.

## 3. Write the options

For each component in scope, a row for each of Retire, Retain, Rehost, Relocate, Replatform, Refactor or re-architect, Repurchase: feasible or not, and why, with `path:start-end` evidence. Then, for each target pattern under consideration: integration points and shared data to decouple, data architecture (shared tables, foreign keys that cross boundaries, synchronization), cross-cutting concerns (authentication, logging, configuration, errors), rules from the inventory (BR ids) that constrain it, top risks and rollback, and rough effort in relative terms only.

Present options with trade-offs. Do not recommend a single one and do not write the decision for the user.

## 4. Gate

Add `## Decision` with `pending`. Stop and ask the architect to choose. Only when they state the decision in this conversation, fill an ADR section: Current state, Selected strategy, Target architecture, Migration scope, Constraints, Risks and mitigations, Alternatives considered. Leave `status: draft`; the user approves the file through `code-modernization`.

End with `## Not verified`: components not examined, rules not read back, unpaged results, languages without structure, and that results describe the ingested snapshot.

Do not call the analysis complete. Do not claim the chosen strategy is faster or lower risk. CoreStory does not run code.
