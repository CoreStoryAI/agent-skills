---
name: spec-kit-companion
description: "Combine GitHub Spec Kit artifacts and commands with CoreStory's architecture-grounded spec-driven workflow. Use when a project uses Spec Kit or .specify artifacts alongside CoreStory."
license: Proprietary
---

# CoreStory Spec Kit Companion

Use GitHub Spec Kit to persist specification artifacts while CoreStory supplies the architectural grounding and validates those artifacts against the real system.

## Preconditions

- Follow the `spec-driven-development` skill for the governing six-phase workflow.
- Confirm the CoreStory MCP is connected and the repository is ingested.
- Confirm Spec Kit is initialized in the repository and its commands are available. Do not install or initialize it unless the user asks you to.

## Workflow mapping

1. **Ground → `/speckit.constitution`:** Query CoreStory for architecture, conventions, invariants, technology decisions, and test strategy. Feed confirmed findings into the constitution.
2. **Specify → `/speckit.specify`:** Write the smallest behavioral delta. Keep acceptance criteria, constraints, and non-goals explicit.
3. **Validate → CoreStory only:** Submit the generated specification to CoreStory. Resolve contradictions, missing dependencies, and pattern violations before planning.
4. **Plan → `/speckit.plan` and `/speckit.tasks`:** Use the validated specification to produce a dependency-ordered plan and test-first task list.
5. **Implement → `/speckit.implement`:** Follow the approved plan and the repository's established conventions.
6. **Verify and capture → CoreStory only:** Verify invariants and acceptance criteria, summarize the implementation, and preserve durable architectural knowledge.

## Required disciplines

- CoreStory findings ground Spec Kit artifacts; Spec Kit does not replace CoreStory validation.
- Phases 3 and 6 have no Spec Kit equivalent and must not be skipped.
- Prefer delta specifications over restating the whole system.
- Treat `.specify/` artifacts as reviewable repository changes. Do not commit or publish them unless the user asks.
- If generated artifacts conflict with confirmed source behavior, surface the conflict and stop for a decision.

## Completion report

State which Spec Kit artifacts changed, which CoreStory findings grounded them, unresolved conflicts, validation performed, and the next human gate.
