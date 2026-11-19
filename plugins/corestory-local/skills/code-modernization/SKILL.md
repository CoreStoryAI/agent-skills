---
name: code-modernization
license: MIT
description: "Route a legacy modernization through its phases one at a time, using phase files in the repo as state and human approval gates between phases. Use for modernization, migration, legacy refactoring, monolith decomposition, or readiness requests, or to ask which modernization phase is next."
---

# Code modernization: router

This skill routes and enforces gates. It does not execute a phase; the phase skill does. Rules: one phase per session; stop at each gate; never skip a phase; never approve a phase yourself.

Preflight: call `status`, then `corpus_info`. If the state is not `snapshot_selected`, the latest ingest `failed`, or the `sao:Rule` count is zero, stop and relay `status.next_step`. Never call `init` or `ingest` without the user's explicit OK.

## Phase state lives in `modernization/` in the repository

One file per phase, each starting with this header (the phase skill writes it):

```
---
phase: <name>
status: draft | approved
date: YYYY-MM-DD
snapshot: <corpus_info snapshot id>
approver: pending | <name>
---
```

| File | Phase | Skill |
|---|---|---|
| `01-assessment.md` | Assessment | `codebase-assessment` |
| `02-rules-inventory.md` | Business rules | `business-rules-extraction` (write its inventory to this path; add the header above it) |
| `03-target-architecture.md` | Strategy and ADR | `target-architecture` |
| `04-work-packages.md` | Sequencing | `decomposition-sequencing` |
| `05-extraction-<wp>.md` | Service extraction design | `monolith-to-microservices`, then `implement-feature` |
| `06-verification-<component>.md` | Behavioral comparison | `behavioral-verification` |

## Detect the phase

List `modernization/*.md` and read each header. The current phase is the first one in the table with no file, or a file whose status is `draft` (it is waiting for approval; do not advance). A file is approved only if its header says `approved` with a named approver. If the user's request names a later phase than the current one, say which file is missing or unapproved and offer the earliest open phase. If `modernization/` does not exist, the current phase is 1. Phases 5 and 6 repeat per work package or component; an approved `04-work-packages.md` opens them.

A phase file whose `snapshot` differs from today's `corpus_info` snapshot id may be stale; say so and let the user decide.

## Route

1. Name the current phase and the prior files you read, then invoke the phase skill. If the skill is not installed, say so and stop.
2. When the phase skill finishes, it has written a `draft` file. Present it and stop. Do not start the next phase in this session.
3. Approval: only on the user's explicit statement in this conversation, set `status: approved`, the approver's name, and the date in that file's header. Then tell the user the next phase and that it starts in a new session.

If the user prefers agent-led, human-gated work with an independent audit, hand off to `vibe-modernization` and stop.

Ask about non-code artifacts that carry rules (JCL, copybooks, job control, lookup tables, stored procedures) when the language is COBOL or SQL-heavy; the graph may have no structure for them.

Do not claim modernization is faster, safer or de-risked. CoreStory reads and indexes code; it does not run or test it, so verification phases compare source and rules and recommend tests.
