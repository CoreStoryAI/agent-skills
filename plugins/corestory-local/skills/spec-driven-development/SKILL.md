---
name: spec-driven-development
license: MIT
description: "Write a feature specification or design for a change to an existing codebase before coding, grounded in CoreStory v3 rule evidence, then plan and implement from it. Use when asked to write a spec, design a change, plan from a spec, or work spec-first, including projects that use GitHub Spec Kit or a .specify folder."
---

# Spec-driven development

Output: `SPEC.md` in the repository root (or the file the user names; with Spec Kit, `.specify/memory/features/<name>/spec.md`). Create it first and append as you go. It is a delta spec: only what changes. Do not commit, push or open a ticket unless asked.

## 1. Preflight

Call `status`, then `corpus_info`. Proceed only if `status.state` is `snapshot_selected`, the latest ingest has not `failed`, and the `sao:Rule` count is above zero. Otherwise say CoreStory evidence is unavailable, relay `status.next_step`, and ask whether to continue from source alone. Never call `init` or `ingest` without the user's explicit OK; `ingest` spends their model-provider money. If `search` says it "could not answer", use `rules_for`, `entity`, `connections` and `read_file`.

## 2. Ground (before writing any spec)

Record in the spec file, each with `path:start-end`:
- Area and patterns: `search(query)`, `connections`, `read_file`.
- Reusable components: what already exists for this need.
- Invariants to preserve: `search(query, kind:"sao:Rule")` with two phrasings per noun or quantity the change touches, then `entity(entity_id, include:["description","evidence"])` and `read_file` on the evidence. Label each data-integrity, state-machine, referential, security or temporal, and include rules enforced in other layers (services, entities, config, SQL, UI validators). Hits are leads.
- Existing acceptance criteria: tests (`list_files(prefix)`), docs and comments you read.
Do not write the spec until these sections exist.

## 3. Specify

In order: invariants (what must not change), reuse (use, do not recreate), delta (new or modified components only), acceptance criteria (testable, outcome-based, each naming the component it exercises). Mark anything you inferred or assumed. If you can ask about missing intent, ask; if not, take the narrowest reading and list the assumption.

## 4. Pre-mortem

CoreStory does not validate specs; you do. For each file the delta touches: `rules_for(path, start_line, end_line)`, following `next_call` until absent, then `entity` on rules that matter and `read_file` to confirm. List conflicts, missing dependencies and failure modes in the spec, and revise it. `rules_for` also returns rules that only support the lines, and an empty page does not mean no rule applies.

## 5. Plan

File-level map: files to change or add, extension points, order by dependency (`connections`), where tests go. Write it in the spec file.

## 6. Implement and verify (when asked to build it)

Write failing tests from the acceptance criteria and the invariants first, implement in plan order, run the suite and record commands and results. For a full implementation cycle use `implement-feature`. Walk every acceptance criterion and invariant and mark each as tested or not. CoreStory reads code; it does not run it.

## Spec Kit (only if `.specify/` exists)

Use Spec Kit for the artifacts and this skill for the grounding: Ground feeds `/speckit.constitution`, Specify is `/speckit.specify`, Plan is `/speckit.plan` then `/speckit.tasks`, Implement is `/speckit.implement`. Validate (step 4) and Verify (step 6) have no Spec Kit command; do them here and edit the artifacts directly. Commit `.specify/memory/` only if asked. If generated text conflicts with source you read, stop and surface it.

## Close out

End the spec with `## Not verified`: rules not read back against source, areas not searched, criteria not tested, and that CoreStory describes the ingested snapshot, not necessarily the working tree. Do not call the spec complete.
