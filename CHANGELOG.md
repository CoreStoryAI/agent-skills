# Changelog

## 1.0.0 — unreleased

- Publish 19 Agent Skills drawn from CoreStory's 18 public playbooks: 16 lifted from playbook skill
  blocks, 2 hand-authored, 1 copied from the published skill reference.
- Fold the Spec Kit companion content into `spec-driven-development` as a `.specify/`-gated section,
  matching the playbook, which presents it as an append rather than a standalone skill.
- Add combined Codex and Claude Code plugin packages.
- Add the OAuth-enabled CoreStory remote MCP configuration. The MCP URL is per-organization, so
  Claude Code prompts for it at install via `userConfig.mcp_url`; Codex requires a manual
  `codex mcp add corestory --url <your org URL>`.
- Add GitHub CLI, `npx skills`, Codex marketplace, and Claude marketplace install paths.
- Add a digest-backed Agent Skills discovery catalog and docs-host export utility.
- Add local and CI release validation.
- License the release under MIT and set every skill's `license` frontmatter to `MIT`.
- Disclose in `SOURCES.md` every playbook side effect that this package converted from a default to
  an explicit request, and every correction applied to the source material.
- Add `constraint-tickets`, a hand-authored skill from CoreStory's measured work on serving
  constraints to coding agents: one-constraint tickets decomposed from a CoreStory spec, plus a GitHub
  Copilot CLI completion hook that refuses to let an agent finish until each checkable constraint
  holds. It is a Claude Code skill whose artifacts are for Copilot CLI; the hook and scripts it writes
  are files for the user to review and install by hand, and the plugin still declares no hooks. Six of
  its claims were brought down to what their sources support before publication; see `SOURCES.md`.
- Rewrite `constraint-tickets` Phase 1 to generate the implementation spec **from the feature
  request** via `refine_document_definition` / `generate_document`, replacing the previous instruction
  to assemble the project's standing tech spec. The two were inconsistent: Phase 2's prompt tells the
  writer that `SPEC.md` is "an implementation spec for an upcoming change", which a system-wide tech
  spec is not, so the skill as published decomposed the wrong document. Phase 1 now also states the
  real MCP contract — the request enters through `definition.instructions` (`generate_document` takes
  no request argument), the result is `document.sections[]` with no assembled markdown, the 25,000-token
  response cap forces paged fetches, a frozen `progress` value is not a stall signal, and no model is
  reported. Phase 3 gains an explicitly-labeled ordering hypothesis (constraint tickets before the
  feature ticket, the blocking set widening as each lands) and the matching `Not measured` disclosure.
  Phases 2 and 4 and both reference files are unchanged.
- Add a quantifier check to `constraint-tickets` Phase 3 (before a constraint is judged violated,
  compare the claim being disproved to the constraint at its written strength). Measured on one fact
  (misread 5 of 8 without, 0 of 8 with; real violations 12 of 12; followed 48 of 48); it did not
  reproduce on 12 other facts, so it is offered as a low-cost guard, not a general fix.
