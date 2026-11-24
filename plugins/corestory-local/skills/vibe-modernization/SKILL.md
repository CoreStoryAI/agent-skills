---
name: vibe-modernization
license: MIT
description: "Route agent-led, human-gated modernization from a legacy system into an existing or new target, one step per session, using phase files in the repo as state. Use for legacy-to-target migration with source-anchored parity checks and an independent conformance audit."
---

# Vibe modernization: router with constraints

> On hosted CoreStory the tools are prefixed `v3_` (e.g. `v3_rules_for`), take a `project_id` (from `list_projects`), and there is no `status`/`init`/`ingest`: start with `v3_corpus_info`. When following a `next_call`, use the `v3_` name and the same `project_id`.

Router and sequencer; it does not execute steps. It also constrains them. Rules: one step per session; stop at each gate; never skip a step; never approve a step yourself; never verify a build this session made (ask for a fresh session). A missing or unindexed target is not a reason to refuse.

Preflight: call `status` if available, then `corpus_info` (hosted: `v3_corpus_info` for the chosen project). If the state is not `snapshot_selected`, the latest ingest `failed`, or the `sao:Rule` count is zero, stop and relay `status.next_step`. Never call `init` or `ingest` without the user's explicit OK. The ingested snapshot is the legacy system.

## Disciplines for every step

- Source decides truth: no claim in a deliverable without a `path:start-end` you read. Where the graph and source disagree, source wins; record both versions as a correction.
- Never modify the legacy system. Target only.
- Where legacy requires something a target convention contradicts, stop and surface it to the user.

## Single-project mode (the default here)

The local server serves one ingested snapshot: the legacy. Read the target's working tree directly instead of querying a second project. Say once that you are in this mode. Every target claim still needs a `path:line` from files you read. If the target has little or no code, start at Step 1 anyway; Step 2B designs it. Do not ingest an empty or tiny target.

## State: files in `modernization/`

Same header and files as `code-modernization` (read its table): `01-assessment.md`, `02-rules-inventory.md`, `03-target-architecture.md`, `04-work-packages.md`, then `05-gap-<ticket>.md`, `05-build-<ticket>.md`, `06-verification-<component>.md`, `07-conformance-<component>.md`. Header fields: phase, status (`draft` or `approved`), date, snapshot, approver. Current step = the first missing or `draft` file. Approval is the user's explicit statement; then you set `approved`, the approver and the date.

## Steps and the skill each uses

1. Recover both architectures: `codebase-assessment` on the legacy. Overlay: list the target's idioms (errors, logging, configuration, transactions, naming, tests) with the files that show each, in `01-assessment.md`. Gate: shared understanding.
2. Behavioral contract: `business-rules-extraction`, output `modernization/02-rules-inventory.md`. Overlay: every rule opened and confirmed at its anchor; classify each PRESERVE, MODIFY or DISCARD. Gate: a domain expert validates, shown the ambiguous, MODIFY and DISCARD rules.
2B. Only if the target is new: `target-architecture`, then stop for the target ADR. Label target statements as decisions, not findings.
3. Backlog: `decomposition-sequencing` (with an existing target there is no `03` file; the target idioms in `01-assessment.md` stand in). Overlay: each package cites a legacy `path:start-end` and a decision log; add a user-story layer above the packages. Gate: story review.
4. Gap analysis per ticket, before any code: write `modernization/05-gap-<ticket>.md` classifying each requirement EXISTS, EXTEND, NEW or CONFLICT, with legacy anchors (`rules_for`, `read_file`) and target anchors (files you read), and the plan: files, tests first, order. CONFLICT first. Gate: human approves the plan.
5. Build: `implement-feature`, output `modernization/05-build-<ticket>.md`. Overlay: tests first, failing for the right reason; match the Step 1 idioms; no new dependency unless the gap file approved it. Gate: review by someone who knows the target.
6. In separate sessions: `behavioral-verification`, then `vibe-conformance-audit`. Equivalence sign-off only when the two agree. If the two files disagree, the audit's reading against source takes precedence; escalate to a human.

Ask about non-code artifacts that carry rules (copybooks, job control, lookup tables, stored procedures).

Do not claim agent-led work is faster or safer. CoreStory reads and indexes code; it does not run or test it.
