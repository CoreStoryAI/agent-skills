# Public sources and disclosed changes

This release republishes and adapts CoreStory's public material into the Agent Skills format.
CoreStory has **18 public playbooks**. They yield **19 skills**:

- **16 lifted** verbatim from the Claude Code skill block embedded in 15 playbooks. The
  `vibe-modernization` playbook contributes two (the router and `vibe-conformance-audit`).
  Below their frontmatter these are byte-for-byte copies of the playbook source, except for the
  changes disclosed under "Behavior changes" and "Corrections" below.
- **2 hand-authored** from playbooks that contain no standalone skill block:
  `spec-driven-test-generation` and `using-corestory-with-jira`.
- **1 copied** from the published skill reference at
  `https://docs.corestory.ai/.well-known/agent-skills/corestory/SKILL.md`.

A 20th skill, `constraint-tickets`, comes from no playbook. It is **hand-authored** from CoreStory's
August–September 2026 measurement program on serving constraints to coding agents, the work behind
CoreStory's 2026-09-08 Microsoft Reactor talk. Its public source is this repository.

| Skill | Provenance | Public source |
| --- | --- | --- |
| `corestory` | copied | [CoreStory Skill Reference](https://docs.corestory.ai/.well-known/agent-skills/corestory/SKILL.md) |
| `bug-resolver` | lifted | [Agentic Bug Resolution](https://docs.corestory.ai/playbooks/agentic-bug-resolution) |
| `implement-feature` | lifted | [Feature Implementation](https://docs.corestory.ai/playbooks/feature-implementation) |
| `feature-gap-analysis` | lifted | [Feature Gap Analysis](https://docs.corestory.ai/playbooks/feature-gap-analysis) |
| `spec-driven-development` | lifted | [Spec-Driven Development](https://docs.corestory.ai/playbooks/spec-driven-development), incorporating [Spec Kit Companion](https://docs.corestory.ai/playbooks/spec-kit-companion) |
| `spec-driven-test-generation` | hand-authored | [Spec-Driven Test Generation](https://docs.corestory.ai/playbooks/spec-driven-test-generation) |
| `generate-tests` | lifted | [Behavioral Test Coverage](https://docs.corestory.ai/playbooks/test-generation/behavioral-test-coverage) |
| `generate-e2e-tests` | lifted | [E2E Test Generation](https://docs.corestory.ai/playbooks/test-generation/e2e-test-generation) |
| `using-corestory-with-jira` | hand-authored | [Using CoreStory with Jira](https://docs.corestory.ai/playbooks/using-corestory-with-jira) |
| `code-modernization` | lifted | [Code Modernization](https://docs.corestory.ai/playbooks/code-modernization) |
| `codebase-assessment` | lifted | [Codebase Assessment](https://docs.corestory.ai/playbooks/modernization/codebase-assessment) |
| `business-rules-extraction` | lifted | [Business Rules Extraction](https://docs.corestory.ai/playbooks/business-rules-extraction) |
| `target-architecture` | lifted | [Target Architecture](https://docs.corestory.ai/playbooks/modernization/target-architecture) |
| `decomposition-sequencing` | lifted | [Decomposition and Sequencing](https://docs.corestory.ai/playbooks/modernization/decomposition-sequencing) |
| `monolith-to-microservices` | lifted | [Monolith to Microservices](https://docs.corestory.ai/playbooks/modernization/monolith-to-microservices) |
| `behavioral-verification` | lifted | [Behavioral Verification](https://docs.corestory.ai/playbooks/modernization/behavioral-verification) |
| `vibe-modernization` | lifted | [Vibe Modernization](https://docs.corestory.ai/playbooks/modernization/vibe-modernization) |
| `vibe-conformance-audit` | lifted | [Vibe Modernization — Conformance Audit](https://docs.corestory.ai/playbooks/modernization/vibe-modernization) |
| `ma-technical-due-diligence` | lifted | [M&A Technical Due Diligence](https://docs.corestory.ai/playbooks/ma-technical-due-diligence) |
| `constraint-tickets` | hand-authored | This repository (no playbook yet); measured program behind CoreStory's 2026-09-08 Microsoft Reactor talk |

All 20 skills carry normalized Agent Skills frontmatter (`name`, `description`, `license`) in place
of whatever the source used. That change is not itemized further below.

## Behavior changes: side effects that were default in the playbooks are opt-in here

An installed skill can act on a repository or an external system without the user re-reading the
playbook first, so this package converts the playbooks' default side effects into actions that
require an explicit request. **This is a real behavior change from the published playbooks**, and in
one case it reverses the playbook's own advice. Every instance is listed here.

| Skill | Playbook default | Behavior in this package |
| --- | --- | --- |
| `bug-resolver` | Phase 6 updates the ticket "if MCP available" and commits with a structured message | Updates the ticket, and commits, only if the user asked; otherwise reports the proposed update and leaves the change uncommitted |
| `implement-feature` | Updates the ticket "if ticketing MCP available" and commits with a detailed message | Both only if the user asked; otherwise reports the proposed update without posting and leaves the change uncommitted |
| `spec-driven-development` | Phase 6 commits with architectural context | Commits only if the user asked |
| `generate-tests` | Completion commits with a structured message | Commits only if the user asked; otherwise leaves the verified tests uncommitted |
| `generate-e2e-tests` | Completion commits with a structured message | Commits only if the user asked |
| `code-modernization` | Phase 4 deliverable is work packages "optionally pushed to Jira/Linear" | Pushes to Jira or Linear only on an explicit request |
| `decomposition-sequencing` | Step 6 creates a migration epic and stories "if Jira/Linear MCP available"; the HITL gate is lead approval before pushing | Creates them only on an explicit request, and states that approving the sequence is not authorization to push it |
| `corestory` | Closing the loop commits with context; the bug-investigation walkthrough and the completion checklist both commit unconditionally | All three are conditional on the user having asked for a commit |

`using-corestory-with-jira` is hand-authored, and it treats Jira writes — creating issues, posting
comments, changing fields, transitioning status — as actions that require an explicit request. The
playbook previously documented comment posting on ticket resolution as the **default** behavior; it
has been amended to match, so the skill and
[the playbook](https://docs.corestory.ai/playbooks/using-corestory-with-jira) now agree that posting
to Jira is user-requested.

## Corrections applied to the source material

These are places where the packaged skill deliberately does **not** match its source, because the
source is wrong.

**Non-existent MCP tools.** The CoreStory MCP server exposes 15 tools. `spec-driven-development`
listed `CoreStory:get_project`, which is not one of them; the line was removed. `list_projects`
already reports project ingestion status, which is what that line claimed to provide. The playbooks
have since been corrected upstream as well, along with `get_project_stats`.

**Cross-skill identifiers.** The playbooks referred to skills by names that no skill in this package
uses. Corrected here, and fixed upstream in the playbooks as well:

| Playbook reference | Corrected to | In |
| --- | --- | --- |
| `spec-driven-dev` | `spec-driven-development` | `code-modernization` |
| "Feature Implementation skill" | `implement-feature` | `feature-gap-analysis` |
| "Business Rules Extraction skill" | `business-rules-extraction` | `feature-gap-analysis` |
| "fix-bug skill" | `bug-resolver` | `implement-feature` |
| `feature-implementation` | `implement-feature` | `vibe-modernization` |
| `e2e-test-generation` | `generate-e2e-tests` | `vibe-modernization` |

**`spec-kit-companion` was folded into `spec-driven-development`.** The playbook presents this
content as an *append* to the existing spec-driven-development configuration
([Spec Kit Companion](https://docs.corestory.ai/playbooks/spec-kit-companion)), not as a standalone
skill, and an earlier revision of this package shipped it standalone anyway — exporting its own
method back out, dropping the four `.specify/memory/` artifact paths it depends on, and reversing
the playbook twice by telling the agent not to commit `.specify/` artifacts and not to initialize
Spec Kit. It is no longer a separate skill. Its content now lives as a "Spec Kit Integration"
section inside `spec-driven-development`, gated on `.specify/` being present, with the artifact
paths restored and both reversals corrected. A reference to "the next human gate" was removed: the
playbook describes no such gate. The upstream playbook's skill block carries the same section, so
`spec-driven-development` remains a faithful lift.

**Content the hand-authored skills had dropped or invented.** `spec-driven-test-generation` regained
the playbook's 8-tool table and its warning not to read the PRD or TechSpec end-to-end, and lost
three unsourced lines: a redirect to `bug-resolver` that is not in the playbook's redirect list, an
instruction to run the smallest relevant tests first (the playbook says to run the full suite after
each batch), and an undocumented output list. `using-corestory-with-jira` regained the Jira MCP
setup guidance — the Rovo endpoint and the community-server options — and five of the seven
documented failure modes it had dropped.

**Unsourced content deliberately retained.** Three lines in `using-corestory-with-jira` have no
basis in the playbook and are kept as general hygiene, not as playbook content: labeling estimates
as estimates, never implying a Jira write succeeded unless the tool confirmed it, and asking the
user to choose when the ticket-to-repository mapping is ambiguous.

**Errors in the copied skill reference.** The `corestory` skill was copied from
`https://docs.corestory.ai/.well-known/agent-skills/corestory/SKILL.md`, which Mintlify generates
from the docs on every deploy rather than anyone authoring it. The generated version contained four
wrong claims, all corrected here: `describe_index` was described as a document-sectioning tool when
it lists file paths and metadata keys in the code index (`get_project_prd` and `get_project_techspec`
take `sections_only`/`sections` for that); a 50KB document threshold and a claim that larger
documents "will timeout" were invented, where the real constraint is the agent's context window;
`semantic_search` and `filter_chunks` were given latency characteristics that are documented nowhere;
and the playbook phase table was reconstructed rather than quoted, collapsing Bug Resolution's six
phases to five and listing two rows that are not phase sequences at all. The docs repository now
carries a committed override so the generated version cannot reintroduce them.

**The CoreStory-unavailable fallback.** Every playbook-embedded skill block opens with a paragraph
telling the agent what to do when CoreStory is not reachable. The four skills not lifted from a
playbook block — `corestory`, `spec-driven-test-generation`, `using-corestory-with-jira` — were
missing it. It has been added to all three, in the canonical wording. (`spec-kit-companion` was
also missing it; it has since been folded into `spec-driven-development`, which carries it.)

**Claims in `constraint-tickets` brought down to their sources.** Before publication, the skill was
reproduced from its text alone by agents that had seen nothing else (a blind ticket writer, a blind
gate builder, a claims audit). The verdict: *"Yes, with a stated qualification … the skill reproduces
the shape, not the instrument … So say: 'we have a skill that writes tickets and hooks in this style,
and a person still writes the assertions.'"* Six claims in the draft were stated more strongly than
their sources, and are corrected in the published version:

| Draft claim | Published wording | Why |
| --- | --- | --- |
| Rule 3 rationale: "Naming the exact spot in one added sentence moved site repairs 1/15 → 0/15" | Rationale is the measured 15-of-15 assertion that passed while nine runs shipped a defect one line above it; the 1/15 → 0/15 is reported as not significant (p = 0.5) | The source calls that difference "not significant, and in the wrong direction," and the arm scoring 0/15 named none of the things the rule bans |
| Hook: "1/15 → 15/15" unqualified | 15 of 15 *on the gate's assertion*, entailed by construction; hazard-addressed 12/15 gated vs 13/15 un-gated | A gate pass implies the criterion passes; the broader measure did not move |
| Ticket 8: "13 of 15, against a control that never opened the file" | 13 of 15 addressed the hazard; the comparator arm read the method in 15 of 15 runs; Ticket 8 is marked measured-but-non-compliant with the review as written | The "never opened the file" control appears in no source; Ticket 8's ask is an order to investigate |
| "byte-identical" as a quality signal | Five identical diffs mean the task admitted one patch — reassuring for correctness, no basis for a rate | The source says byte-identity is "useless for estimating a rate" |
| "Ours once blocked the only correct repair in a batch" (uncited) | Kept, cited to the site-repair record ("first pass blocked all 15, including r4"), and paired with the false pass: the first refund gate passed a diff that shorted the customer 30.00 of 70.00 | Both directions have happened; both are now cited |
| "none named one off-path tax defect" | "…at constraint level, though the generator surfaced that tax subsystem in about one draft in five" | The categorical form was superseded in the source |

The same review found the draft did not say what it is (a Claude Code skill producing Copilot CLI
artifacts), where the decomposition must run (a fresh invocation whose only context is the spec),
that its own example file hands a Shopizer writer the answer, or that the gate script — not the
fixture — owns the verdict. All four are now stated in the skill. Structural gaps it proposed but
did not fix are listed in the skill's "Known limits" section.

Source snapshot date: 2026-09-02; `constraint-tickets` added 2026-09-07.
