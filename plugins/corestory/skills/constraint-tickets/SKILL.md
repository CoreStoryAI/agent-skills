---
name: constraint-tickets
description: "Turn a CoreStory spec into constraint-style tickets, one constraint per ticket, and generate the GitHub Copilot CLI completion hook that refuses to let an agent finish until each checkable constraint holds. Use when asked for constraint tickets, to turn this spec into tickets, spec to tickets, break the spec into tickets, decompose the spec, one constraint per ticket, a completion hook, a stop hook, an agentStop hook, a Copilot hook, a refusal gate, or to not let the agent finish until a constraint holds; or for any request to make an agent act on facts a feature request never states."
license: MIT
---

# Constraint Tickets — from a CoreStory spec to tickets an agent will act on

**If you do not detect that you have access to CoreStory (e.g., `list_projects` fails or is unavailable), ask the user to verify that their MCP or API connection is properly configured and that this repository has been ingested. If the user has not yet created a CoreStory account, direct them to create one and upload their repo at [app.corestory.ai](https://app.corestory.ai).**

**What this is and where it runs.** This is a skill for Claude Code, or any agent that loads Agent
Skills, and it produces artifacts for **GitHub Copilot CLI**: a set of tickets, a gate script, an
`agentStop` script, and a hooks JSON. Copilot CLI does not load this skill. It only runs the hook the
skill produces, after a person has reviewed and installed it.

Agents do the task they are given and treat everything else as reference. A constraint handed over
*alongside* a task — as a spec in the working tree, a search index, a chat answer, or an instruction
file the agent is ordered to read — does not become work. The same constraint handed over *as* the
task does. In the measurement program behind this skill, one constraint converted 5 of 5 as its own
ticket where the same fact, attached to a feature task as an instruction file the agent was ordered
to read first, converted 2 of 5, and as an 85 KB spec in the working tree 1 of 5. This skill produces
the shape that was measured to work, and the hook that checks it on the way out.

**What a constraint is.** One checkable statement about the finished system that the request never
stated, sourced from knowledge of the system rather than from the requester. Both kinds count: an
invariant the code currently violates ("a refund must be recorded as a refund") and a behavior the
change must have or preserve ("a partial refund must not mark the whole order refunded").

**Where the constraints come from.** Agents do not inherit a system's constraints. Their exploration
starts at the ticket and radiates outward, inside one session, so it reaches what it can walk to and
nothing else. CoreStory's spec is generated from the whole system ahead of any task, so it can carry
facts a task-directed walk never reaches. This skill is the conversion step between the two.

## First run

You need: a CoreStory project with finished ingestion, reachable over MCP; GitHub Copilot CLI on the
machine that will run the coding agent; and the target repository's own build toolchain — for a
Maven/Java repository, a warm local Maven cache and a JDK pinned to the version the build targets,
not whatever `mvn` picks up from the shell.

Install: `claude plugin marketplace add corestoryai/agent-skills` then
`claude plugin install corestory@corestory`, and invoke it from Claude Code by asking to "decompose
the spec into constraint tickets". It is not a Copilot CLI skill; Copilot CLI only runs the hook it
produces.

Out: `SPEC.md` and its hash, `TICKETS.md`, one frozen file per ticket, `PROVENANCE.md`,
`CONSTRAINTS.md`, a gate script, an `agentStop` script, and a hooks JSON.

By hand afterward: write every assertion yourself — the skill ships no fixture and no build command.
Run the validations in Phase 4 before arming the hook. Review the tickets.

## Prerequisites

- A CoreStory project with completed ingestion, reachable over the CoreStory MCP server
  (`list_projects`, `get_project_techspec`, `get_project_prd`, `semantic_search`, `send_message`).
- For the hook: GitHub Copilot CLI on the machine that will run the agent, and a way to execute a
  check against a working tree — a build command and a fixture, test, or script that returns
  pass/fail. This skill does not supply those; the user writes them for their repository.

## Phase 1 — Get the spec, and only the spec

1. `list_projects` → pick the project. `get_project_techspec` with `sections_only=true` first, then
   fetch the sections that describe current behavior, affected components, risks, failure modes, and
   acceptance criteria. If a feature request exists, keep it in a separate file; the tickets below are
   written from the spec's *constraints*, not from the request's wording.
2. Assemble the fetched sections into one `SPEC.md`, in the order the spec lists them, each under its
   own heading, in an otherwise empty working directory. **No source tree in that directory, and no
   other files.** Two operators who assemble the sections differently will produce different files
   and different hashes; record the section list you used in `PROVENANCE.md`.
3. Hash it: `shasum -a 256 SPEC.md`. Record the hash in `PROVENANCE.md`. Do not paste the hash into
   the tickets themselves — a ticket that carries attached context fails rule 2 below.

## Phase 2 — Decompose into constraint tickets

**Who runs it.** The decomposition must run in a fresh agent invocation whose only context is the
directory holding `SPEC.md` — no source tree, no other files, no prior conversation. The "name the
area, never the site" rule below is enforced by that isolation and by nothing else: an agent that
can see the source will cite it. The measured runs used a separate invocation with a sandboxed home
directory and an opaque working directory. If you decompose inside your own session with the
repository open, you are not running the measured procedure.

**Do not read `references/ticket-examples.md` before writing.** It holds the measured exemplar for
one specific constraint in one specific repository (Shopizer). A writer decomposing a Shopizer spec
who has seen it is reproducing the exemplar, not deriving a ticket, and any demonstration of this
skill on Shopizer is not independent derivation. Read it after the review step, as a check on
register.

Run the decomposition with this prompt, verbatim. Save the prompt text you used to
`decompose-prompt.txt` so it can be hashed.

> SPEC.md in this directory is an implementation spec for an upcoming change. It is the only material
> you have; there is no source tree here to read. Read it in full, then decompose it into the set of
> implementation tickets the engineering team should work from.
>
> - Each ticket is a single concern — one outcome that one engineer can own end to end. Do not merge
>   unrelated concerns to keep the count down, and do not split one concern across several tickets.
> - Cover the spec. Every distinct piece of required work or required correction lands in exactly one
>   ticket, including ones that look small, incidental, or like clean-up.
> - Write each ticket the way a product or engineering lead writes one: plain business language,
>   stating the outcome required and why it matters. Two to five sentences of body.
> - Do not write code. Do not cite line numbers, quote diffs, or instruct the engineer to change a
>   specific symbol or value. Naming the area or component in question is fine.
> - Each ticket must stand on its own. Assume the reader has not seen this spec.
>
> Write the result to TICKETS.md as `## Ticket N — <short title>` followed by the body.

Then **review every ticket against the four rules that were measured**, and fix any that fail. Where
the prompt and a rule collide — the prompt says not to split one concern, rule 1 says to split a
ticket carrying two constraints — the rule wins.

| rule | why (measured) |
|---|---|
| **One constraint per ticket.** If a ticket carries two, split it. | A ticket converts exactly what it names and nothing else — 0 of 5 runs touched a second defect four lines from the one they fixed, and no run mentioned it. |
| **The constraint is the whole ticket, not a rider.** No "while you're there," no attached context, no "see also the spec." | The same constraint riding on a feature task converted 2 of 5 with the agent ordered to read it first; alone, 5 of 5. |
| **Name the area, never the site.** No file paths, no method names, no line numbers, no identifiers. (*Site* = the exact code location that has to change; *area* = the component or subsystem it lives in.) | An assertion that asked about a line of code passed 15 of 15 while nine of those runs shipped a money defect one line above it. Naming a site gets the site touched and says nothing about the behavior. Naming the exact spot in a measured arm did not help either: site repairs went 1 of 15 to 0 of 15, a difference its source calls not significant (p = 0.5). State what must be true, not where. |
| **Symptom and consequence, then the ask.** "X records Y wrongly; that breaks Z; correct X so that…" The ask states one checkable property of the finished system, in the imperative. A ticket that asks for investigation, review, or strengthening states no constraint. | This is the register of the ticket that converged five of five; all five diffs were identical, which means the task admitted one patch — reassuring for correctness, not a rate. |

Freeze each ticket as its own file (`tickets/NN-<slug>.txt`), hash each with `shasum -a 256`, and
write a `PROVENANCE.md` naming the spec hash, the hash of `decompose-prompt.txt`, the section list
used to assemble `SPEC.md`, the model and settings that ran the decomposition, and which spec
sections each ticket draws on (most draw on several; list them all). **Say plainly in
`PROVENANCE.md` which tickets are spec-derived and which, if any, a person wrote.**

## Phase 3 — Split the list: tickets, assertions, flags

The list is the ticket set from Phase 2. One constraint per ticket, so the tickets are the list.
Every constraint on it goes to at least one of three places:

- **Ticket** — the constraint is work someone must do. Every constraint gets one.
- **Assertion** — the constraint is *checkable* against a working tree (a fixture, a test that runs
  against production code paths, a static predicate). These become the gate.
- **Flag** — the constraint is real but out of scope for the ticket the agent is working. The hook
  surfaces it as an advisory instead of refusing (measured: 4 of 5 runs surfaced a pre-existing defect
  during unrelated work with the flag armed, 0 of 5 without it).

Write the split as a table in `CONSTRAINTS.md`: constraint · ticket file · assertion (yes/no, how) ·
flag-only (yes/no). This table is the artifact the architecture rests on.

## Phase 4 — Generate the completion hook

Follow `references/hook-template.md` exactly. In summary:

1. **One assertion per constraint**, each runnable against a working tree and returning pass/fail
   with a message that names the file, the numbers, and the constraint. The message is the product:
   it is what the agent reads next. The skill supplies the contract and the script skeletons; the
   assertion itself, the build command, the classpath, and the JDK pin are the user's own work.
2. **A gate script** with the exit-code contract `0` pass · `1` block · `3` tampered · `4` could not run.
   It copies the live tree's patch to a pristine worktree *outside* the agent's directory, builds,
   runs the fixture there, and never runs the agent's own tests. **The gate script owns the verdict.**
   The fixture prints values and may always exit 0; never derive the gate's exit code from the
   fixture's. **Every error path blocks.** A gate that cannot verify must refuse, not pass.
3. **An `agentStop` hook** that runs the gate and emits `{"decision":"block","reason":"<message>"}` on
   any non-zero exit. Install it user-level, in `$COPILOT_HOME/hooks/` — `COPILOT_HOME` is the
   directory Copilot CLI reads its configuration from, `~/.copilot` by default — not in the
   repository the agent edits.
4. **Validate both ways before arming**, and record all six results: the broken tree → BLOCK; a
   known-good fix → PASS; a directory that is not this project → PASS (out of scope); the fixture
   renamed or edited → TAMPER; the reference repository pointed at a nonexistent path → BLOCK with a
   message saying nothing was verified; a wrong fix that reaches the expected number by breaking the
   case that was already correct → BLOCK with its own message. A gate that has not passed a known-good
   fix will refuse a correct one.
5. **Scope the blocking gate to the ticket it was written for.** Off that ticket, install the flag
   mode (`postToolUse` advisory) instead; a blocking gate armed against pre-existing defects the
   agent was not asked to fix refuses every turn.

## What this skill can and cannot claim

- **Measured** (GitHub Copilot CLI, one repository, `claude-sonnet-5` unless stated):
  the ticket style — 1 of 5 to 5 of 5 on one constraint, all five diffs identical, and 13 of 15
  addressing a second constraint on a different model; the completion hook — 1 of 15 to 15 of 15 on
  the assertion it carried, same ticket, same model, where the 15 of 15 is 15 of 15 *on the gate's
  assertion* and is entailed by construction (a gate pass implies the criterion passes), and the
  broader hazard-addressed measure in the gated arm was 12 of 15 against 13 of 15 without the gate;
  the flag — 4 of 5 surfaced a pre-existing defect during unrelated work, 0 of 5 without.
- **Not measured:** that a ticket carrying two constraints converts both; that any generated spec
  names every constraint — five specs named 9 to 11 of 12 pre-registered hazards, and none named one
  off-path tax defect at constraint level, though the generator surfaced that tax subsystem in about
  one draft in five; that the hook produces *correct* code beyond the assertions it checks. A
  passing gate is not a working system: one assertion scored 15 of 15 while nine runs shipped a
  defect one line above it. Assert the behavior, not the symptom.
- Five identical diffs mean the task admitted exactly one patch. That is reassuring for correctness
  and says nothing about a rate.

Never present output of this skill as verified. Present it as tickets and a gate, in the shape that
was measured to work, ready for a person to review.

## Known limits

Found when a stranger reproduced the skill from its text alone. Listed as limits, not as done work.

- **The Phase 2 review has no assigned reviewer.** The default is self-review by the writer, and the
  review has a known false-positive mode: applied as written, it rejects the measured second ticket in
  `references/ticket-examples.md`, whose ask is an order to investigate.
- **Phase 4 supplies no assertion language, build command, worked example, or fixture.** Every
  assertion is the user's own work. A gate built from the template by someone who assumes the
  fixture's exit code is the verdict never blocks — and still passes three of the four original
  validations, which is why the two extra validation rows exist.
- **Flag mode has no script here.** It is described in one paragraph of the template.
- **`PROVENANCE.md` is thinner than the measured reference.** The reference also recorded a
  launch-order selection rule for the case where more than one decomposition exists.
- **The exit code and integrity manifest do not protect against a regenerated manifest.** The
  manifest cannot be in the manifest.

## References

- `references/ticket-examples.md` — the 593-byte ticket that converted 5 of 5, a second measured
  ticket, the spec passage that did *not* convert when attached, and a hand-written ticket for an
  off-path defect. Read after writing, not before.
- `references/hook-template.md` — hooks JSON, the fail-closed `agentStop` script skeleton, the gate
  contract, the six-row validation checklist, and the Copilot CLI behaviors measured on 1.0.80–1.0.82.
