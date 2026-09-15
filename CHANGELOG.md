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
- **`constraint-tickets` Phase 1 now sends `options: {"polish": false}`, and this is not optional.**
  `polish` defaults to **true** on `refine_document_definition`, and a polished section is rewritten
  end to end by a second LLM pass that never saw the codebase — of which **only the first 20,000
  characters are kept; the remainder is dropped from the stored result**. Both halves defeat the
  procedure: the rewrite puts prose between the index and the ticket writer on a method whose premise
  is fidelity to what the index found, and the truncation silently amputates the long sections
  (**Affected Components** and **Risks and Failure Modes** have both been seen cut off mid-reference
  in the field). This is a different limit from the 25,000-token response cap already documented: that
  one is read-side and paging recovers from it, this one destroys content before it is stored and no
  re-fetch brings it back. Step 2 also corrects a related instruction — the returned `options` block
  must be **kept**, not stripped with the per-section fields (`research_strategy`, `requires_signal`)
  that `generate_document` actually rejects — and step 4 adds a per-section truncated-tail check.
  Which setting the measured runs used is not recorded, so the spec-quality figures are now disclosed
  as possibly describing polished specs.
- **Separate `constraint-tickets`' harness-neutral gate from its harness-specific binding.** The gate
  is a plain executable with an exit-code contract and was always portable; only the ~15 lines wiring
  it to a completion event are not. `references/hook-template.md` now leads with that split and ships
  a **Claude Code binding** (`Stop`, **exit code 2**, message on **stderr**) alongside the measured
  Copilot CLI one (`agentStop`, `{"decision":"block"}` on stdout, exit 0). The two are near inverses,
  and porting either unchanged fails **open** and silently, so the difference is documented twice and
  a seventh validation check — watch a real session actually be refused — is added, because the six
  existing rows invoke the gate directly and cannot catch a broken binding. The Claude Code binding is
  **documented, not measured**; VS Code still has no binding, as its agent hooks are in Preview with
  no documented completion event.
- **Add a "When not to use" section to `constraint-tickets`.** Field testing put a bot-written CI
  failure for a Spring 6 → 7 upgrade through the skill; it is the wrong input on three counts at once,
  and nothing in the skill said so. The section routes framework and platform migrations and lockstep
  dependency upgrades to `code-modernization` / `codebase-assessment`, routes bot-generated issues to
  `bug-resolver`, and defines what "verbatim request" means for an issue tracker (body only, no title,
  no comments, no appended CI content).
- **Ship `constraint-tickets/references/decompose-prompt.txt`** as canonical bytes, sha256
  `3bdd16dd…234574c`, published in the skill. Phase 2 requires the prompt's hash in `PROVENANCE.md`,
  but the prompt existed only inside a SKILL.md blockquote, so every operator who retyped it produced
  different bytes — different line wraps, quote marks and em dashes — and therefore an unreproducible
  hash. The file is now what you run; the blockquote is for reading.
- **Other `constraint-tickets` fixes from the same field report.** Phase 1 gains a step 0 that pins
  which CoreStory server and organization is in use and **stops to ask when more than one is
  reachable** — every organization exposes identical tool names, so a spec could be generated against
  the wrong one with nothing downstream revealing it. Phase 2 gains a per-harness isolation recipe and
  a provenance field recording whether `HOME` was sandboxed. Phase 1 gains a prescribed run-file
  layout, and the gate's exclusion list is extended from three instruction files to every run artifact
  (`REQUEST.md`, `TICKETS.md`, `CONSTRAINTS.md`, `PROVENANCE.md`, `definition.json`, the ticket tree),
  which otherwise ride into the patch the gate judges — including `SPEC.md`, whose presence in the
  working tree is the arm that converted 1 of 5. "First run" gains a five-row preflight, since phases
  1–3 need none of the build toolchain and an operator could previously reach Phase 4 before finding
  the machine could not run one.
