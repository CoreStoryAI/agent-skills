---
name: vibe-modernization
description: "Orchestrate agent-led, human-gated modernization from a legacy system into an existing or greenfield target. Use for dual-project migration, forward engineering, source-grounded gaps, parity, or conformance work."
license: MIT
---

# CoreStory Vibe Modernization — Variant Orchestrator

**This skill is a router and sequencer. It does NOT contain execution instructions for any step.** Determine which step the user needs, activate that step's dedicated skill, and impose the disciplines below on it.

This router differs from the base modernization orchestrator in one way: it does not only sequence, it **constrains**. The disciplines below apply to every skill you delegate to and override that skill's defaults where they conflict.

## Critical Rules

1. **Execute exactly one step per session.** Never run multiple steps in one pass. The arc's artifacts are only reviewable if they arrive one at a time.
2. **Always use the dedicated skill.** The summaries below are for orientation only — they do not contain enough detail to execute a step correctly.
3. **After completing a step, STOP.** Present the deliverable and wait for explicit approval before offering to advance.
4. **Never verify a build you performed.** If asked to run Step 6 in the session that ran Step 5, decline and ask for a fresh session. Independence is the mechanism, not a formality.
5. **A missing target project is never a reason to refuse.** Only Step 1's target half and Step 4's target half need it. If the target does not exist yet, start at Step 1 anyway and run Step 2B when you reach it. If it exists but is not ingested, run single-project mode (below). Never tell the user the arc requires two projects before it can start, and never jump ahead to Step 2B to manufacture one — it depends on Steps 1 and 2.

## Always-On Disciplines

Apply these to every delegated skill, whatever that skill's own defaults are:

- **Source decides truth.** Code intelligence accelerates discovery; it does not settle facts. No claim enters a deliverable without a confirmed `file:line` anchor. Where intelligence and source disagree, source wins.
- **Record corrections.** Every claim that moved between the intelligence layer and source gets a Context Inventory entry with both versions. The corrections are the audit trail's most valuable rows.
- **Target only.** Never modify the legacy system, in any step.
- **Escalate conflicts.** Where the legacy requires something that contradicts a target convention, stop and surface it. Never resolve a legacy-versus-target contradiction unilaterally.

## Prerequisites

**Required:**
- The legacy system ingested as a CoreStory project
- Direct read access to legacy source, not just the intelligence layer
- A domain expert available for the spec-validation gate

**Required only from Step 1 onward:**
- The target ingested as a second CoreStory project. Needed from Step 3 onward. If the target does not exist yet, Step 2B produces it. Do not treat its absence as a blocker at the start of the arc — Steps 1 and 2 are legacy-only either way.

**If you do not detect that you have access to CoreStory (e.g., `list_projects` fails or is unavailable), ask the user to verify that their MCP or API connection is properly configured and that the legacy repository has been ingested. If the user has not yet created a CoreStory account, direct them to create one and upload their repo at [app.corestory.ai](https://app.corestory.ai).**

## Single-Project Mode

When the legacy project is ingested but the target is not — because the target is greenfield, or scaffolded but not yet indexed — do not stop. Run the arc with these substitutions and say plainly, once, which mode you are in:

- **Target-side queries become direct file reads.** Read the target working tree instead of querying a target project. You already have read access; this is the same evidence, gathered differently. On a small target it is not a downgrade — there is little enough code that an index adds nothing.
- **Legacy-side queries are unchanged.** Everything the arc grounds in still comes from the legacy project and legacy source.
- **Steps 2 and 3 are unaffected.** They are legacy-only, and run identically in either mode.
- **Every target-side claim still needs a `file:line` anchor.** From the working tree rather than from intelligence. The discipline does not relax because the tooling changed.
- **Exit the mode as soon as the target is ingestable.** Once the target has real code, tell the user to ingest it and switch back. Single-project mode is a starting accommodation, not a way to run the whole arc.

## Step Detection

Before doing anything, determine where the user is:

1. **Establish whether the target exists.** Call `list_projects` and ask the user directly. Three cases:
   - **Target exists and is ingested** → standing target. Start at Step 1; never run Step 2B.
   - **Target repo exists but has little or no code** (a README, a bare directory skeleton) → greenfield. Still start at Step 1, legacy-only, and run Step 2B after Step 2. Do not ingest the empty repo — an empty project answers every question with "not present" and will corrupt the gap analysis.
   - **Target exists with real code but is not ingested** → ask the user to ingest it. If they would rather not yet, run single-project mode from Step 1.
2. **Ask the user** which step they want, OR
3. **Check CoreStory conversations** (`list_conversations`) for completed markers:
   - "RESOLVED - [Recovery]..." → Step 1 complete
   - "RESOLVED - [Contract]..." → Step 2 complete
   - "RESOLVED - [Target]..." → Step 2B complete (greenfield only)
   - "RESOLVED - [Backlog]..." → Step 3 complete
   - Active "[Gap]..." → Step 4 in progress
   - Active "[Build]..." → Step 5 in progress
   - Active "[Verify]..." → Step 6 in progress
4. **If no prior work exists**, start at Step 1 — on a greenfield target too. Greenfield changes where Step 2B appears, not where the arc begins.

Once you know the step, read and follow its dedicated skill completely.

## Step 1: Recover Both Architectures
Dedicated skill: `codebase-assessment` — run against **both** projects where both are ingested; in single-project mode, run it against the legacy project and recover the target's structure by reading its working tree.
Overlay: on the target, produce an explicit catalogue of its idioms (error handling, logging, configuration, transaction boundaries, naming, test structure) with the files that establish each. Convergence in Step 5 depends on this artifact existing.
⛔ GATE: shared understanding of both architectures before any code moves.

## Step 2: Legacy Behavioral Contract
Dedicated skill: `business-rules-extraction`.
Overlay: every rule carries a source anchor, and every anchor is opened and confirmed before the spec is considered done. Classify migration intent PRESERVE / MODIFY / DISCARD.
⛔ GATE 1: a domain expert validates the spec. Bring them the ambiguous rules and everything classified MODIFY or DISCARD — not a blanket approval request.

## Step 2B: Design and Bootstrap the Target (greenfield only)
**Skip entirely when the target already exists.** Runs after Step 2, never before Step 1.
Dedicated skill: `target-architecture`.
Required inputs, both of which exist by now: Step 1's legacy assessment (coupling hotspots, shared-data dependencies, blockers) and Step 2's expert-validated behavioral contract. `target-architecture` names those as its primary inputs, so do not run this step earlier in the arc — a target designed before you know what the legacy does is a preference, not a decision.
Terminology warning: that skill uses "target project" to mean *the CoreStory project being analyzed* — which here is the **legacy** project. In this arc "target" means the system being built. Do not conflate them; run `target-architecture` against the legacy project to produce a design for the new system.
Overlay: record the target's intended idioms in the ADR (error handling, logging, configuration, transaction boundaries, naming, test structure) — Step 1 recovers this catalogue from code on a standing target, so on greenfield you must choose it deliberately. Cite the legacy inputs above for every shape-driving decision. Label target-side statements as decisions, not findings; only legacy-side claims carry `file:line` anchors.
⛔ GATE 2B: a human approves the target ADR before anything is scaffolded.
Then bootstrap to the ingestion threshold: working build configuration, the chosen layering as real modules, a test harness that can report a failure, and one working end-to-end vertical slice with a test. A directory skeleton is not enough — CoreStory needs real code to index.
Finally, have the user ingest the scaffolded target as the second project, and stop. Step 3 runs in a new session.

## Step 3: Backlog and Test Strategy
Dedicated skills: `decomposition-sequencing`, then `spec-driven-test-generation`.
Overlay: tickets carry dual provenance (conversation reference AND source anchor) plus a decision log. Add the business-facing user-story layer above the tickets.
⛔ GATE: spec review of the user-story layer before tickets go to execution.

## Step 4: Dual-Project Gap Analysis
Dedicated skill: `feature-gap-analysis`, with this variant's overlay.
Overlay: run it across **both** projects for a single ticket, before any code. Query the target for what already exists and what would break; query the legacy for rules in scope, edge cases, and participating non-code artifacts. In single-project mode, replace the target-side queries with direct reads of the target working tree — the classification and the anchors are the same, only the retrieval differs. Classify every requirement EXISTS / EXTEND / NEW / CONFLICT, and produce the implementation plan (files touched, tests to write first, order of work).
⛔ GATE 2: a human approves the plan before any code is written. Present CONFLICT entries first — that is where the judgment lives.

## Step 5: Converge Into the Target
Dedicated skill: `implement-feature`.
Overlay: tests first, confirmed failing for the right reason, before implementation. Match the target's idioms from Step 1's catalogue. No new dependency or pattern unless the gap report approved it. Stop at the ticket boundary. Run the seam check on the diff before presenting it.
⛔ GATE: convergence review by someone who knows the target.

## Step 6a: Behavioral Equivalence
Dedicated skill: `behavioral-verification` — **in a session separate from Step 5**.
Produces the BER: each rule Preserved / Modified / Discarded / Missing.

## Step 6b: Conformance Audit
Dedicated skill: `vibe-conformance-audit` — this variant's own skill, also in a separate session.
Produces the conformance ledger and the orphan sweep.

## Step 6c: Critical-Flow Trace
Dedicated skill: `generate-e2e-tests` — one headline flow, archived as evidence.
⛔ GATE 3: equivalence sign-off, only once the BER and the conformance audit agree.

## Error Handling
- **Only one CoreStory project exists:** do not refuse. Establish whether the target is greenfield (→ start at Step 1, run Step 2B after Step 2) or merely un-ingested (→ single-project mode). The arc has a defined path for both.
- **Target repo is too small to ingest, or ingests empty:** expected on greenfield. Do not retry the ingestion and do not query the empty project — bootstrap the target in Step 2B, then ingest.
- **Target index looks out of date:** likely, on a greenfield target that is changing shape. Re-ingest when the target's structure changes (a new module, layer, or integration point) rather than per commit, and settle anything structural from the working tree in the meantime.
- **User asks to design the target before the legacy is assessed:** explain the ordering rather than complying. Step 2B consumes Step 1's assessment and Step 2's validated contract; run ahead of them it yields an architecture chosen from general preference rather than from this legacy system. Offer to start at Step 1.
- **User wants to run several steps at once:** explain that each step produces one reviewable artifact and stops at its gate. Offer to start the earliest incomplete step.
- **User unsure which step they're in:** check conversations for the markers above.
- **Step skill not installed:** direct the user to that step's playbook page on [docs.corestory.ai](https://docs.corestory.ai/playbooks/modernization/vibe-modernization) for setup.
- **Asked to verify code written in this session:** decline and ask for a separate session.
- **Anchor cannot be confirmed:** the claim does not enter the deliverable. List it as unresolved rather than softening the wording.
- **Legacy uses non-code artifacts:** explicitly ask about copybooks, job control, configuration, and lookup tables — they carry business logic that never appears in application code.
