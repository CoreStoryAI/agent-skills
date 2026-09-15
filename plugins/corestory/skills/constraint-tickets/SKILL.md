---
name: constraint-tickets
description: "Turn a CoreStory spec into constraint-style tickets, one constraint per ticket, and generate the completion hook that refuses to let an agent finish until each checkable constraint holds. Use when asked for constraint tickets, to turn this spec into tickets, spec to tickets, break the spec into tickets, decompose the spec, one constraint per ticket, a completion hook, a stop hook, an agentStop hook, a Copilot hook, a refusal gate, or to not let the agent finish until a constraint holds; generate the implementation spec from this feature request, spec from a feature request then tickets; or for any request to make an agent act on facts a feature request never states."
license: MIT
---

# Constraint Tickets — from a CoreStory spec to tickets an agent will act on

**If you do not detect that you have access to CoreStory (e.g., `list_projects` fails or is unavailable), ask the user to verify that their MCP or API connection is properly configured and that this repository has been ingested. If the user has not yet created a CoreStory account, direct them to create one and upload their repo at [app.corestory.ai](https://app.corestory.ai).**

**What this is and where it runs.** This is a skill for Claude Code, or any agent that loads Agent
Skills. It produces a set of tickets, a gate script, and a completion hook that binds the gate to
whichever harness will run the coding agent. The harness that runs the coding agent does not load
this skill; it only runs the hook the skill produces, after a person has reviewed and installed it.

**The gate is harness-neutral; only the binding is not.** The gate script — its exit-code contract,
its pristine worktree, its fixture, its message — is a plain executable and cares about no harness.
What differs per harness is the fifteen lines that bind it: which event fires on completion, and how
that event says *block*. `references/hook-template.md` gives the neutral contract plus one binding
per harness. **GitHub Copilot CLI is the only binding behind which there are measurements.** A
Claude Code binding is given and rests on documented behavior, not measured behavior. The two are
close to inverses — on Copilot CLI a bare non-zero exit blocks nothing and you must emit
`{"decision":"block"}`; on Claude Code exit code 2 is itself the block — so do not carry a hook from
one to the other unchanged.

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
nothing else. CoreStory's index is built from the whole system ahead of any task; the implementation
spec it generates for a request draws on that index, which is how the spec can name a constraint the
request never states. This skill is the conversion step between that generated spec and tickets an
agent will act on.

## When not to use this skill

The input this skill is built for is **a short feature request written by a person, which does not
state its own constraints**. "Add Google SSO authentication to this application" is the shape. The
value the skill adds is naming what such a request leaves unsaid. Given an input that already states
its constraints, or one whose constraints cannot be carried by a ticket, the skill adds nothing and
its measured shape does not apply.

Stop and route elsewhere when any of these holds:

- **A framework, platform, or runtime migration, or a lockstep dependency upgrade.** Spring 6 → 7,
  Java 8 → 17, a JDK or database major version. These fail the skill on three counts at once: the
  checkable constraints are "it builds" and "the existing suite passes", which is not what the gate
  does; no single constraint ticket leaves a tree that builds, which breaks the one-ticket-at-a-time
  order of work in Phase 3; and the blast radius is the whole repository rather than one behavior.
  → `code-modernization`, or `codebase-assessment` to size it first.
- **A bot-generated issue** — a CI failure report, a dependency-bot PR, a scanner finding. The body
  is a machine artifact, not a request, and Phase 1 forbids editing it. A CI report saved verbatim
  as `REQUEST.md` sends a build log into the generator's `instructions`, and if it carries its own
  agent workflow the agent may follow the issue instead of this skill. → `bug-resolver` for a real
  defect; for a CI failure, fix the build.
- **The request already states its constraints** — a well-written user story with acceptance
  criteria. There is nothing unsaid for the index to supply. Decompose it directly.
- **A constraint that no fixture can check**, and no other constraint in the set can either. The
  gate is the half of this skill that was measured to move a rate. With nothing checkable, you have
  tickets and no gate, which is worth doing but is not this skill's result.
- **No completed CoreStory ingestion of the repository the change lands in.** Phase 1's whole
  premise is the index. Without it, the generator is guessing from the request, which is the thing
  the skill exists to improve on.

**What "verbatim request" means for an issue tracker.** Take the issue **body** only, as markdown,
excluding the title, comments, labels, and any CI or bot content appended to it. If removing bot
content would leave less than a couple of sentences of human writing, that issue is not an input to
this skill — see the second bullet above. If you cannot get to a verbatim human request without
editing, stop and ask the requester for one. Record in `PROVENANCE.md` exactly what you took and
what you left, with the issue URL.

## First run

You need: a CoreStory project with finished ingestion, reachable over MCP; a harness with a
completion hook on the machine that will run the coding agent; and the target repository's own build
toolchain — for a Maven/Java repository, a warm local Maven cache and a JDK pinned to the version the
build targets, not whatever `mvn` picks up from the shell.

Install: `claude plugin marketplace add corestoryai/agent-skills` then
`claude plugin install corestory@corestory`, and invoke it from Claude Code by asking to "decompose
the spec into constraint tickets". The harness that runs the coding agent does not load this skill;
it only runs the hook this skill produces.

**Preflight — check these before Phase 1, not at Phase 4.** Phases 1–3 need only CoreStory, so an
operator can do a day's work and reach the gate before discovering the machine cannot build one.
Check and report all five up front, and say which phases can proceed without them:

| check | why |
|---|---|
| the target repo is a **git clone with a `HEAD`**, not a copied directory | the gate diffs the live tree against `HEAD`; a copy has nothing to diff |
| the repo's **build tool** is installed and on `PATH` | the gate builds in its own worktree |
| a **JDK (or runtime) pinned to what the build targets**, not the newest installed | a Java 17 build under JDK 21 fails in the gate and not in the agent's session |
| the **harness that will run the coding agent** is installed, and its completion hook is supported | the binding is harness-specific; see `references/hook-template.md` |
| you can **run the repo's build once, green, before any change** | a gate cannot distinguish your change from a build that was already broken |

Missing any of the first three blocks Phase 4 only. Phases 1–3 can go ahead and produce the tickets.

Out: `REQUEST.md`, `definition.json`, `SPEC.md` and its hash, `TICKETS.md`, one frozen file per
ticket, `PROVENANCE.md`, `CONSTRAINTS.md`, a gate script, an `agentStop` script, and a hooks JSON.

By hand afterward: write every assertion yourself — the skill ships no fixture and no build command.
Run the validations in Phase 4 before arming the hook. Review the tickets.

## Prerequisites

- A CoreStory project with completed ingestion, reachable over the CoreStory MCP server
  (`list_projects`, `refine_document_definition`, `generate_document`,
  `get_document_generation_result`, `get_project_techspec`, `get_project_prd`, `semantic_search`,
  `send_message`). Phase 1 runs on the first four. `get_project_techspec` and `get_project_prd` are
  for the human reviewer in Phase 2 — they are not Phase 1's input.
- For the hook: a harness with a completion hook on the machine that will run the agent, and a way to
  execute a check against a working tree — a build command and a fixture, test, or script that
  returns pass/fail. This skill does not supply those; the user writes them for their repository.

## Phase 1 — Generate the spec from the feature request, and only the spec

**Every CoreStory MCP tool below takes a required `context` string of 15-25 words, third person,
describing why the call is being made. It is analytics metadata and does not affect generation.**

**Input.** The feature request, verbatim, as the requester wrote it. Save it as `REQUEST.md` in an
otherwise empty working directory and hash it (`shasum -a 256`). Do not edit it, expand it, or add
what you know about the system. The point of the exercise is to measure what the intelligence adds
to the request as written.

0. **Establish which CoreStory server you are talking to, and say so.** Every CoreStory organization
   exposes the *same* tool names (`list_projects`, `generate_document`, and the rest), and an agent
   can have several connected at once without any of them being distinguishable by name — Claude Code
   loads claude.ai account connectors into every project, so a project-local server is easily the
   third of three. Nothing downstream would reveal a spec generated against the wrong organization.
   **If more than one CoreStory server is reachable, stop and ask the user which one to use.** Do not
   pick. Record the server name, its transport and URL (or the connector it came from), and the
   organization it belongs to, in `PROVENANCE.md`, before the first call.
1. `list_projects` → pick the project holding the repository the change will land in, and confirm
   ingestion has finished — require `ingestion_status == "completed"` explicitly. Older projects
   return `null` rather than `"completed"` or `"failed"`; `null` is undocumented and is not the same
   as failure, but it is not confirmation either, so do not run on one. If CoreStory is unreachable,
   stop and say so (see the note at the top of this file). Record `project_id` and the project's
   name alongside the server, and confirm with the user that the project is the repository the
   change will land in — a name collision across organizations is exactly the failure step 0 guards.
2. `refine_document_definition` with five custom sections, in this order, names verbatim:
   **Scope · Affected Components · Constraints and Invariants · Risks and Failure Modes · Acceptance
   Criteria.** Each section's one-line description asks for the system's *current* behavior relevant
   to the request, with evidence back to source, and states that the request is the only input.
   **Do not add a section that names a subsystem.** The measured definition named none; a section
   called "Tax handling" puts the answer in the question. Pass the verbatim text of `REQUEST.md`
   in the definition's top-level `instructions` field: that is the only channel the request has to
   the generator —
   `generate_document` takes no separate request argument.

   **Send `options: {"polish": false}`. This is not optional for this skill.** `polish` defaults to
   **true**, and a polished section is rewritten end to end by a second LLM pass that never saw the
   codebase — and **only the section's first 20,000 characters reach that pass; anything past them is
   dropped from the result.** Both halves are wrong here. The rewrite puts prose between the index
   and the ticket writer on a procedure whose entire premise is fidelity to what the index found,
   and the truncation silently amputates the long sections — **Affected Components** and **Risks and
   Failure Modes** are the two that run long, and they have been seen cut off mid-sentence in a
   closing reference list. This truncation is **not** the 25,000-token response cap in step 4: that
   one is a read-side limit you recover from by paging, this one drops the content before it is ever
   stored, and no amount of paging brings it back. A section that arrives truncated was generated
   truncated. Set the flag and the whole section is returned unpolished and uncut.

   The tool returns `{"valid": true, "definition": {...}}`; save the inner `definition` object as
   `definition.json` and hash it. The server hands back more than it was sent. Two different things
   come back, and they are handled differently:
   - **Per-section fields** the caller never supplied — `research_strategy` and `requires_signal`
     among them — which `generate_document`'s own section schema then **rejects**. Strip these.
   - **A top-level `options` block**, filled in with the server's defaults (`detail_level`,
     `max_tokens_per_section`, `reference_validation`, and `polish`). **Do not strip this block** —
     it is where your `"polish": false` lives, and `generate_document` accepts it. Confirm
     `options.polish` reads `false` in what you send on. Per-section `polish` comes back as `null`,
     meaning *inherit the global*, so the one top-level flag is enough; leave the nulls alone.

   So what you send on is the returned definition with the rejected per-section fields stripped and
   `options` intact, and `definition.json` is a hash of what was **sent**, not of what the server
   validated. Record which fields you stripped, and record `options.polish` in `PROVENANCE.md`.
3. `generate_document` with `project_id` and the validated definition (which already carries the
   request text in its `instructions`). Record the `run_id` the moment it is returned. Generation
   is long-running, and the wall time varies with the repository: three runs on this definition
   took 1038 s and 629 s on Shopizer and 468 s on a small VB6 repository. Budget for twenty minutes
   and do not read a slow run as a failed one. Poll
   `get_document_generation_result` until `status` is `complete` or `failed`; while running it also
   returns a `progress` percentage. **A `progress` number that stops moving is not a stall
   signal** — it has been seen frozen at the same value across four consecutive polls spanning six
   minutes, and non-monotonic within a single run, both times on runs that completed normally. The
   stopping rule is `status`, not `progress`: a run still `queued` after several polls is not
   progressing — say so and stop. **Do not substitute another document.**
4. The result carries no assembled markdown. `document.sections` is a list of
   `{name, level, content, structured_content, sources, subsections}`; assemble `SPEC.md` by
   writing `document.title` as a level-1 heading, then each section's `name` as a heading at its
   `level` followed by its `content`, verbatim. Do not edit the content. Two operators who
   assemble the sections differently produce different bytes and different hashes from the same
   run — the assembly rule above exists to make the hash reproducible, so state in `PROVENANCE.md`
   that you followed it. **A poll with no
   `sections` filter exceeds the server's 25,000-token response cap and returns a truncation
   notice in place of the document** — fetch the sections one at a time with the `sections`
   argument, or page with `limit`/`offset`.

   **Then check each section for a truncated tail** before you assemble. Read the last line of every
   section: a section that ends mid-sentence, mid-path, or mid-list — rather than at a full stop —
   was cut, and the two long sections (**Affected Components**, **Risks and Failure Modes**) are
   where it shows up. Paging does not fix this one and re-fetching returns the same bytes. If you
   find a cut tail, the run was generated with `polish` on (step 2); the content is gone from the
   stored result and the only remedy is to regenerate with `"polish": false`. **Do not assemble a
   `SPEC.md` from truncated sections and do not patch the gap by hand** — a spec the operator
   completed is no longer a measurement of what the index supplied. Record in `PROVENANCE.md`: the
   `REQUEST.md` hash, the `definition.json` hash, `run_id`, `document.id` (there is no top-level
   `document_id`), `metadata.generated_at`, `metadata.generation_time_seconds`,
   `metadata.template_hash` — the only version-like field the result carries — the value of
   `options.polish` for the run, and the result of this tail check per section. **The tool reports no
   model.** Also record the `SPEC.md` hash.
5. Check before continuing: the **Scope** section of `SPEC.md` names the thing the request asked
   for. If it does not, the generation did not take the request. Do not decompose it.
6. **Do not use the project's standing tech spec (`get_project_techspec`) or PRD as `SPEC.md`.**
   They describe the system, not the change, and Phase 2's prompt assumes an implementation spec for
   an upcoming change. A person may consult them during the Phase 2 review. They are not the input.

The directory holds `REQUEST.md`, `definition.json`, `SPEC.md`, `PROVENANCE.md` and nothing else.
No source tree. Before Phase 2, move `SPEC.md` alone into a fresh directory: the decomposition
invocation sees the spec and only the spec. The request's wording does not reach the ticket writer;
the tickets are written from the spec's constraints.

**Where these directories live.** "An otherwise empty working directory" is a constraint on what the
decomposer can see, and where you put it decides whether that holds. Use this layout:

```
<repo>/constraint-tickets/runs/<date>-<slug>/     run artifacts; ADD TO .gitignore
    phase1/   REQUEST.md  definition.json  SPEC.md  PROVENANCE.md
    phase3/   TICKETS.md  CONSTRAINTS.md  tickets/NN-<slug>.txt
~/corestory-constraint-tickets/decompose/<run>/   SPEC.md ALONE — outside the repo (Phase 2)
~/corestory-constraint-tickets/gate/<run>/        gate, fixture, manifest — outside the repo (Phase 4)
```

Two rules make it work, and both have a measured reason:

- **The Phase 2 decompose directory is outside the repository.** Inside it, the decomposer can reach
  the source tree and will cite it, which breaks "name the area, never the site" — the rule that
  isolation, and nothing else, enforces.
- **The gate lives outside the tree the agent edits**, so the agent cannot read or rewrite the thing
  judging it, and so the gate's own files never appear in the patch it judges.

Run artifacts may sit inside the repo, gitignored, but **everything under `constraint-tickets/runs/`
must be excluded from the patch the gate judges** — `SPEC.md` above all. A spec left readable in the
working tree is the arm that converted 1 of 5; leaving it there while the gate runs recreates the
weakest measured condition by accident. See `references/hook-template.md` §3 for the exclusion list.

**What this step is measured to do, and not.** Generated from a four-sentence refund request with
this definition, five independent specs named 9 to 11 of 12 pre-registered hazards at the level of
the subsystem, and 4 to 6 of 12 at the level of a constraint specific enough to act on (EVIDENCE B1).
The two subsystems the request never named — tax and notification — were the two the spec almost
never reached (B2). Generation starts from the request, so it inherits some of the request's blind
spots. It is where the measured tickets came from; it is not a guarantee of completeness.

## Phase 2 — Decompose into constraint tickets

**Who runs it.** The decomposition must run in a fresh agent invocation whose only context is the
directory holding `SPEC.md` — no source tree, no other files, no prior conversation. The "name the
area, never the site" rule below is enforced by that isolation and by nothing else: an agent that
can see the source will cite it. The measured runs used a separate invocation with a sandboxed home
directory and an opaque working directory. If you decompose inside your own session with the
repository open, you are not running the measured procedure.

**Isolation recipe.** Copy `SPEC.md` alone into `~/corestory-constraint-tickets/decompose/<run>/`,
then start a fresh agent *in that directory*:

| harness | how |
|---|---|
| **Claude Code** | `cd` to the directory and run `claude` there in a new terminal. Add `--strict-mcp-config` so no MCP server loads, and note that the session still reads `~/.claude/CLAUDE.md` and user-level memory. `HOME=$(mktemp -d) claude` sandboxes those too and is what the measured runs did. |
| **Copilot CLI** | `cd` to the directory and run `copilot -p "$(cat ../decompose-prompt.txt)"`. `~/.copilot/instructions/` still loads unless `COPILOT_HOME` is pointed at an empty directory. |
| **VS Code / an IDE agent** | Open the isolated folder as its own window. The workspace is then the folder, but user-level instructions and memory still load; this is close to the procedure, not the procedure. |

The gap that survives every row but the sandboxed-`HOME` one is user-level instructions and memory.
**Record in `PROVENANCE.md` which of these you used, and say plainly whether the home directory was
sandboxed.** A decomposition run with the repository open is still useful output — it is just not a
measured run, and the provenance should not let the two be confused later.

**Do not read `references/ticket-examples.md` before writing.** It holds the measured exemplar for
one specific constraint in one specific repository (Shopizer). A writer decomposing a Shopizer spec
who has seen it is reproducing the exemplar, not deriving a ticket, and any demonstration of this
skill on Shopizer is not independent derivation. Read it after the review step, as a check on
register.

Run the decomposition with this prompt, verbatim. **Use the shipped file — do not retype or
copy-paste it out of this page.** `references/decompose-prompt.txt` is the canonical bytes:

```
sha256  3bdd16ddaee3cdb5daf0463fa73cd0e8dfab231b4fb8d162eded6f404234574c
```

Copy that file next to the isolated `SPEC.md` and verify the hash (`shasum -a 256`) before running.
Phase 2 asks you to record the prompt's hash in `PROVENANCE.md`, and a hash is only worth recording
if two operators can produce the same one: a prompt lifted out of the blockquote below picks up
different line wraps, quote marks, and em dashes, and hashes differently every time. The text is
reproduced here for reading. The file is what you run.

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

## Phase 3 — Route the list: tickets, assertions, flags

The list is the constraint set from Phase 2 — one statement per constraint. Each constraint is routed
by three questions, and a constraint can land in more than one place:

1. **Does the code violate it today, or must the change newly satisfy it?** If yes, it is work: it
   becomes a **ticket**, one constraint per ticket. If the code already satisfies it, it does not
   become a ticket — a ticket that says "keep X true" is a check, not work.
2. **Can it be checked against a working tree** — a fixture, a test that runs against production code
   paths, a static predicate? If yes, it becomes an **assertion** in the gate, whether or not it also
   became a ticket. An already-satisfied, checkable constraint becomes an assertion only: it is
   protected while the change lands.
3. **Is it in scope for the ticket the agent is working?** In scope, the assertion **blocks**. Out of
   scope, it **flags** — the hook surfaces it as an advisory instead of refusing (measured: 4 of 5
   runs surfaced a pre-existing defect during unrelated work with the flag armed, 0 of 5 without it).

So a constraint may be a ticket *and* an assertion (violated today and checkable — the refund label,
the tax base); an assertion only (already true and checkable); a ticket only (violated, but not
checkable by a fixture — "the customer is notified"; a person reviews it); or a flag only (outside the
current ticket).

Write the routing as a table in `CONSTRAINTS.md`: constraint · satisfied today (yes/no) · ticket file ·
assertion (yes/no, how) · block / flag, per ticket. This table is the artifact the architecture rests
on. Ticket and assertion are the two measured mechanisms; the routing beyond them — assertion-only,
ticket-only, flag — is the design the results imply, not a measured result.

**Order of work.** Work the constraint tickets before the feature ticket, and work each one alone:
its own agent session, its own change, merged before the next begins. The reasoning: constraints on
pre-existing code are the ground the feature stands on — fix how a refund is recorded before building
a cap that reads the record. Each session sees only its own ticket, but it works on a tree that
already holds the previous fixes, so the tree does the coordination the tickets do not. Constraints
that describe the feature's *new* behavior cannot come first — there is nothing yet to constrain —
so they go into the feature ticket's gate as blocking assertions rather than into tickets that
precede it.

**The gate follows the order.** On a constraint ticket, the gate blocks on that ticket's assertion
only and carries every other assertion in flag mode; a blocking gate armed against constraints the
agent was not asked to fix refuses every turn. Once a constraint ticket has merged, its assertion
flips from flag to block on every later ticket — it is now a known-true property of the tree, and
the gate's job is to keep it true. On the feature ticket, block on every landed constraint plus the
new-behavior constraints; flag the rest. Rule 4 makes this safe: an assertion becomes blocking only
after it has passed on a known-good tree, and the merge of its constraint ticket is exactly when
that becomes true.

This ordering is a hypothesis. Nothing about sequencing has been measured; the results behind this
skill are single tickets and single-assertion gates. It is stated here because the alternative —
constraint tickets and the feature ticket landing in no particular order, none aware of the others —
has an obvious failure mode, and because the gate design above is what the measured results imply.

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
3. **A completion-hook binding** that runs the gate when the agent tries to finish and turns a
   non-zero exit into a refusal carrying the gate's message. The binding is the only harness-specific
   part, it is about fifteen lines, and **the way it signals a block differs per harness — on Copilot
   CLI a bare non-zero exit blocks nothing and you emit `{"decision":"block","reason":…}` from an
   `agentStop` hook; on Claude Code exit code 2 from a `Stop` hook *is* the block and stderr is the
   message.** Take the binding for your harness from `references/hook-template.md` §2; do not port
   one across. Install it **user-level and outside the repository the agent edits**
   (`$COPILOT_HOME/hooks/`, default `~/.copilot`; or `~/.claude/settings.json`), so the agent can
   neither read nor delete the thing judging it.
4. **Validate both ways before arming**, and record all six results: the broken tree → BLOCK; a
   known-good fix → PASS; a directory that is not this project → PASS (out of scope); the fixture
   renamed or edited → TAMPER; the reference repository pointed at a nonexistent path → BLOCK with a
   message saying nothing was verified; a wrong fix that reaches the expected number by breaking the
   case that was already correct → BLOCK with its own message. A gate that has not passed a known-good
   fix will refuse a correct one.
5. **Scope the blocking gate to the ticket it was written for.** Off that ticket, install the flag
   mode (a post-tool advisory) instead; a blocking gate armed against pre-existing defects the
   agent was not asked to fix refuses every turn, and widen the blocking set as constraint tickets
   land (Phase 3, Order of work).
6. **Re-run validation on the harness you will actually arm.** The six rows in step 4 test the gate,
   which is harness-neutral. They do not test the binding. Confirm separately, on your harness, that
   a blocking verdict really stops the agent and that the message reaches it — the failure mode is a
   binding that fails *open*, where the gate correctly returns 1 and the agent finishes anyway
   having been told nothing. Only the Copilot CLI binding has been measured; treat any other as
   unverified until you have watched it refuse.

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
  defect one line above it. Assert the behavior, not the symptom. Also not measured: that working
  the constraint tickets before the feature ticket produces a better result than any other order, or
  that a landed constraint's assertion, flipped to blocking, prevents a later ticket from undoing
  it. Both are the design the results imply; neither has a cell.
- Five identical diffs mean the task admitted exactly one patch. That is reassuring for correctness
  and says nothing about a rate.
- **Every measured cell was run against Copilot CLI.** No result here was produced on Claude Code, in
  VS Code, or on any other harness. The gate is harness-neutral and the ticket results are about
  ticket text rather than about a harness, so both should carry over; that expectation has no cell
  behind it. The binding certainly does not carry over — see Phase 4 step 6.
- **`polish` was not a controlled variable.** Phase 1 now requires `"polish": false`, because a
  polished section is rewritten by a second model and truncated at 20,000 characters. Which setting
  the measured runs used is not recorded, and the default is `true`. So the spec numbers above
  (9–11 of 12, 4–6 of 12) may describe polished specs. That does not put the ticket and gate results
  in question — those were measured downstream of a fixed spec — but it does mean the spec-quality
  figures have not been reproduced under the setting the skill now mandates.

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
- **Only the Copilot CLI binding has been run.** The Claude Code binding in the template is built
  from documented hook behavior — `Stop` blocks on exit code 2 and the hook's stderr reaches the
  model — and has not been watched refusing a real session. Whether Claude Code's `Stop` also accepts
  a `{"decision":"block","reason":…}` JSON shape is not settled here, which is why the binding uses
  exit 2 and stderr, the path the documentation states plainly.
- **No binding exists for VS Code or other IDE agents.** VS Code's agent hooks are in Preview and its
  documentation does not describe a completion event equivalent to `agentStop`. Phases 1–3 work
  there; Phase 4 does not have a recipe.
- **The isolation recipe does not fully isolate outside the sandboxed-`HOME` row.** User-level
  instruction files and memory still load in every other variant.

## References

- `references/ticket-examples.md` — the 593-byte ticket that converted 5 of 5, a second measured
  ticket, the spec passage that did *not* convert when attached, and a hand-written ticket for an
  off-path defect. Read after writing, not before.
- `references/hook-template.md` — the harness-neutral gate contract, one binding per harness
  (Copilot CLI, measured; Claude Code, documented), the fail-closed script skeletons, the six-row
  validation checklist, and the Copilot CLI behaviors measured on 1.0.80–1.0.82.
- `references/decompose-prompt.txt` — the Phase 2 prompt, canonical bytes,
  sha256 `3bdd16ddaee3cdb5daf0463fa73cd0e8dfab231b4fb8d162eded6f404234574c`. Run this file; do not
  retype the prompt.
