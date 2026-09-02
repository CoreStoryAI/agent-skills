---
name: code-modernization
description: "Orchestrate legacy-system modernization with CoreStory. Use for modernization, migration, legacy refactoring, monolith decomposition, or readiness requests; route one phase at a time through human approval gates."
license: Proprietary
---

# CoreStory Code Modernization — Orchestrator

**This skill is a router and sequencer. It does NOT contain execution instructions for any phase.** When this skill activates, your job is to determine which phase the user needs, activate the dedicated skill for that phase, and enforce the gate between phases.

## Critical Rules

1. **Execute exactly one phase per session.** Never run multiple phases in a single pass.
2. **Always use the dedicated phase skill.** The summaries below are for orientation only — they do not contain enough detail to execute the phase correctly. Read and follow the dedicated skill for the active phase.
3. **After completing a phase, STOP.** Present the deliverable and wait for the user to explicitly approve before offering to advance to the next phase.
4. **Never skip phases.** Each phase depends on the outputs of the one before it.

## Activation Triggers

Activate when user requests:
- Code modernization or legacy modernization
- System migration or codebase migration
- Legacy refactoring or re-architecture
- Monolith decomposition or monolith-to-microservices
- Modernization assessment or readiness evaluation
- Any request containing "modernize", "migration", "legacy", "monolith", "mainframe"

## Prerequisites

- CoreStory MCP server configured
- At least one CoreStory project with completed ingestion (the legacy codebase)
- Read access to the repository for cross-referencing findings

**If you do not detect that you have access to CoreStory (e.g., `list_projects` fails or is unavailable), ask the user to verify that their MCP or API connection is properly configured and that this repository has been ingested. If the user has not yet created a CoreStory account, direct them to create one and upload their repo at [app.corestory.ai](https://app.corestory.ai).**

## Phase Detection

Before doing anything, determine where the user is in the process:

1. **Ask the user** which phase they want to work on, OR
2. **Check CoreStory conversations** (`list_conversations`) — look for completed phase markers:
   - "RESOLVED - [Assessment]..." → Phase 1 complete
   - "RESOLVED - [Business Rules]..." → Phase 2 complete
   - "RESOLVED - [Architecture]..." → Phase 3 complete
   - "RESOLVED - [Decomposition]..." → Phase 4 complete
   - Active "[Extraction]..." conversations → Phase 5 in progress
   - Active "[Verification]..." conversations → Phase 6 in progress
3. **If no prior work exists**, start at Phase 1.

Once you know the target phase, read and follow its dedicated skill completely.

---

## Phase 1: Codebase Assessment

**Purpose:** Evaluate the legacy system's architecture, dependencies, tech debt, and modernization readiness.

**Dedicated skill:** Use the `codebase-assessment` skill and follow its full workflow.

**Deliverable:** Modernization Readiness Report

**⛔ GATE: Do not proceed to Phase 2 until the user has reviewed the Readiness Report and given explicit go/no-go approval.**

---

## Phase 2: Business Rules Inventory

**Purpose:** Extract, catalog, and verify all business rules embedded in the legacy system.

**Dedicated skill:** Use the `business-rules-extraction` skill and follow its full workflow. If the skill is not installed, refer to the [Business Rules Extraction playbook](https://docs.corestory.ai/playbooks/business-rules-extraction) for setup instructions.

**Deliverable:** Business Rules Inventory (BR-XXX format)

**⛔ GATE: Do not proceed to Phase 3 until the user has reviewed the Business Rules Inventory and confirmed completeness.**

---

## Phase 3: Target Architecture & Strategy

**Purpose:** Evaluate modernization strategies (the 7 Rs), define the target architecture, and document the decision.

**Dedicated skill:** Use the `target-architecture` skill and follow its full workflow.

**Deliverable:** Architectural Decision Record (ADR)

**⛔ GATE: Do not proceed to Phase 4 until the architect or tech lead has approved the ADR.**

---

## Phase 4: Decomposition & Sequencing

**Purpose:** Break the modernization into discrete, sequenced work packages with dependency mapping and acceptance criteria.

**Dedicated skill:** Use the `decomposition-sequencing` skill and follow its full workflow.

**Deliverable:** Sequenced work packages. Push them to Jira or Linear only when the user explicitly requests that external write.

**⛔ GATE: Do not proceed to Phase 5 until the engineering lead has approved the sequence.**

---

## Phase 5: Iterative Execution (per component)

**Purpose:** Execute the modernization for each component following the Transform → Coexist → Eliminate pattern.

**Dedicated skill:** Use the `spec-driven-development` skill — it's the foundation for all forward engineering with CoreStory, and it generates the per-component delta specs this phase requires.

For architecture-to-architecture variants, also load the matching skill:
- Monolith to microservices → `monolith-to-microservices`

**Deliverable:** Modernized component with coexistence infrastructure

**⛔ GATE: Do not proceed to Phase 6 for a component until the delta spec has been reviewed and the Transform phase is functionally complete.**

---

## Phase 6: Behavioral Verification (per component)

**Purpose:** Verify that the modernized component preserves every business rule from the Phase 2 inventory.

**Dedicated skill:** Use the `behavioral-verification` skill and follow its full workflow.

**Deliverable:** Behavioral Equivalence Report

**⛔ GATE: Do not retire the legacy component until the domain expert or engineering lead has validated the Equivalence Report.**

---

## Error Handling

- **Project not found:** List available projects, ask user to specify
- **Generic answers from CoreStory:** Narrow queries with specific component names from Tech Spec
- **User unsure which phase they're in:** Check CoreStory conversations for completed phase markers (see Phase Detection above)
- **User wants to jump ahead:** Explain the dependency chain and what outputs are missing. Offer to start from the earliest incomplete phase.
- **Phase skill not installed:** Direct the user to the relevant playbook page on [docs.corestory.ai](https://docs.corestory.ai/playbooks/code-modernization) for setup instructions.
- **Legacy system uses non-code artifacts:** Explicitly ask about JCL, copybooks, CICS, VSAM — CoreStory surfaces these if prompted
