---
name: vibe-conformance-audit
license: MIT
description: "Run an independent, read-only audit of delivered code against legacy source at the grain of single behaviors, with verdicts and an orphan sweep, written to modernization/07-conformance-COMPONENT.md. Use to find stubs, missing behavior or divergence, in a session that did not write the code."
---

# Vibe conformance audit

> On hosted CoreStory the tools are prefixed `v3_` (e.g. `v3_rules_for`), take a `project_id` (from `list_projects`), and there is no `status`/`init`/`ingest`: start with `v3_corpus_info`. When following a `next_call`, use the `v3_` name and the same `project_id`.

Output: `modernization/07-conformance-<component>.md`. Read-only: never edit code under audit.

## Refuse to run

If this session wrote or edited the code under audit, stop and ask for a fresh session. Do not proceed because the user says it is fine. If you have already read `modernization/06-verification-*.md` in this session, say your independence is compromised.

## 1. Preflight and inputs

Call `status` if available, then `corpus_info` (hosted: `v3_corpus_info` for the chosen project). Proceed only if `status.state` is `snapshot_selected`, the latest ingest has not `failed`, and the `sao:Rule` count is above zero; otherwise relay `status.next_step`. Never call `init` or `ingest` without the user's explicit OK. The snapshot is the legacy system; read the delivered code from the working tree.

Read `modernization/02-rules-inventory.md` (the spec; must be `approved`). Ask for the component and where its code lives. Do not open `06-verification-*.md` yet. Start the file with the header (`phase: conformance-<component>`, `status: draft`, `date`, `snapshot` from `corpus_info`, `approver: pending`).

## 2. Oracle rules

Legacy source is the only oracle, not the spec, the tests or the equivalence file. Passing tests are not evidence. Read the legacy lines yourself with `read_file`.

## 3. Atoms and verdicts

Split each in-scope rule into atoms, the smallest behaviors that can be present, absent or wrong (three branches are three atoms). One verdict per atom, citing both the delivered `path:line` and the legacy `path:start-end` you read:

- `DELIVERED`: implemented and matches legacy.
- `STUBBED`: code exists but does no work (constant, log and return, empty branch, TODO, unconditional success).
- `MISSING`: no implementation.
- `DIVERGES`: implemented differently; state both behaviors.
- `UNVERIFIABLE`: reading cannot settle it; state what would.

Do not soften a verdict because code looks reasonable. If the scope is too large for atom grain, narrow it and say what was left out; never sample silently. If an atom has no legacy counterpart, flag a spec defect. If you cannot find the legacy code, mark UNVERIFIABLE; do not infer legacy from the new code.

## 4. Orphan sweep

Read the other way: `rules_for(path, start_line, end_line)` (follow `next_call`) and `read_file` on the legacy files in scope. List behaviors present in legacy but absent from the inventory, with anchors, and whether the omission looks deliberate. `rules_for` also returns supporting rules; check each.

## 5. Reconcile

Only now open `06-verification-<component>.md` if it exists. For each atom where it disagrees with your verdict, resolve against legacy source and state which artifact is wrong. A Preserved or Equivalent over a STUBBED atom is a finding. Stop; leave `status: draft` for human review.

End with `## Not verified`: atoms not read on both sides, unpaged results, and that CoreStory describes the ingested snapshot.

Do not call the audit complete. CoreStory does not run code; no verdict here is a runtime result.
