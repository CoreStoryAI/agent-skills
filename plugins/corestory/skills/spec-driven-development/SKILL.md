---
name: spec-driven-development
description: "Use CoreStory for architecture-grounded spec-driven development. Invoke when writing a feature specification, designing a change, planning from a spec, or implementing through a specification-first workflow, including projects that use GitHub Spec Kit or .specify artifacts."
license: MIT
---

# Spec-Driven Development with CoreStory

Execute the six-phase spec-driven development workflow. Every spec must be grounded in the actual architecture before implementation.

**If you do not detect that you have access to CoreStory (e.g., `list_projects` fails or is unavailable), ask the user to verify that their MCP or API connection is properly configured and that this repository has been ingested. If the user has not yet created a CoreStory account, direct them to create one and upload their repo at [app.corestory.ai](https://app.corestory.ai).**

## CoreStory MCP Tools
- `CoreStory:list_projects` — list available projects
- `CoreStory:create_conversation` — start specification thread
- `CoreStory:send_message` — query code intelligence
- `CoreStory:get_project_prd` — access product requirements
- `CoreStory:get_project_techspec` — access technical specifications
- `CoreStory:rename_conversation` — mark as completed

When instructions say "Query CoreStory", use `CoreStory:send_message`.

## Phase 1: Ground — Before Writing Any Spec
1. Gather requirements (from ticket or user)
2. Select CoreStory project (`CoreStory:list_projects`, verify "completed")
3. Create conversation: "Spec: #[ID] — [description]"
4. Query CoreStory for:
   - Architectural patterns in the relevant area
   - Existing services and reusable components
   - Invariants and constraints that must be preserved (categorize:
     data-integrity, state-machine, referential, security, temporal)
   - Existing acceptance criteria for the impacted area (from
     PRD user stories) — capture as raw AC + enforcing code refs
   - Design history and past attempts

If a Business Rules Inventory exists for this codebase, pull
the `Invariants` and `Acceptance Criteria` fields from BR-IDs
adjacent to the change scope BEFORE issuing the queries above —
that's authoritative content already extracted.

**Do not proceed to Phase 2 until you have documented: patterns, existing services, invariants (categorized), existing ACs, and history.**

## Phase 2: Specify — Delta Specification
Write the spec constrained by Phase 1 findings:
1. **Invariants first** — what must NOT change (categorized)
2. **Reuse section** — existing components to use, not recreate
3. **Delta section** — only new/modified components
4. **Acceptance criteria** — testable, referencing specific existing
   components. In modernization context, pull from work-package +
   BR Inventory's AC fields; net-new ACs only for `[NEW]` / `[CHANGE]`
   tagged behaviors.

This is a delta spec: only what changes. Do NOT re-specify existing functionality.

## Phase 3: Validate — Architectural Pre-Mortem
Submit the spec to CoreStory for validation:
1. Check for architectural conflicts
2. Check for missing dependencies
3. Run failure mode analysis (what could go wrong?)
4. Revise spec based on findings

**Do not proceed to Phase 4 until CoreStory has validated the spec.**

## Phase 4: Plan — File-Level Implementation Map
Query CoreStory for:
1. Exact file paths for each new component
2. Extension points and base classes
3. Implementation order based on actual dependencies
4. Test file locations

## Phase 5: Implement — TDD with Validation
1. Write failing tests from BOTH acceptance criteria AND invariants
   (AC tests assert outcomes; invariant tests assert post-conditions
   that must hold after any operation)
2. Implement in dependency order from Phase 4
3. Validate each component with CoreStory
4. Run full test suite — no regressions

## Phase 6: Verify & Capture
1. Walk the AC list one-by-one — each AC must have a corresponding
   outcome-based test and a confirmed implementation site
2. Walk the invariant list one-by-one — each invariant must have an
   asserted post-condition test
3. If the user requested a commit, commit with architectural context; otherwise leave the verified implementation uncommitted
4. Rename conversation → "COMPLETED"
5. Update ticket

## Key Principles
- Ground before Specify — always
- Invariant-first, reuse-first
- Delta specs, not greenfield specs
- Validate before Plan
- Conversation IS the living spec record

## Spec Kit Integration (only if `.specify/` exists)

Skip this section entirely when the project does not use GitHub Spec Kit. When `.specify/`
is present, persist artifacts through Spec Kit while CoreStory supplies the grounding and
does the validating. CoreStory before Spec Kit at every phase.

| Artifact | Location | Created by |
| --- | --- | --- |
| Constitution | `.specify/memory/constitution.md` | `/speckit.constitution` |
| Feature spec | `.specify/memory/features/{name}/spec.md` | `/speckit.specify` |
| Technical plan | `.specify/memory/features/{name}/plan.md` | `/speckit.plan` |
| Task breakdown | `.specify/memory/features/{name}/tasks.md` | `/speckit.tasks` |

Phase mapping: Ground -> `/speckit.constitution`; Specify -> `/speckit.specify`;
**Validate -> CoreStory only** (Spec Kit has no validation command -- paste the contents of
`spec.md` into a CoreStory message and ask for an architectural pre-mortem, then edit the
artifact directly); Plan -> `/speckit.plan` then `/speckit.tasks`; Implement ->
`/speckit.implement`; **Verify & Capture -> CoreStory only** (no Spec Kit equivalent).

Phases 3 and 6 have no Spec Kit command and must not be skipped -- they are the gap this
integration exists to close. The constitution is the highest-leverage artifact; invest the
most query time there and update it after features ship. Version-control the artifacts:
commit `.specify/memory/` so specs are PR-reviewable alongside the code. If a generated
artifact conflicts with confirmed source behavior, surface the conflict and stop for a
decision -- the CoreStory conversation is the source of truth for architectural reasoning.

If Spec Kit is not yet initialized and the user wants it, install and initialize it:

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
specify check
specify init . --ai <your agent>
```
