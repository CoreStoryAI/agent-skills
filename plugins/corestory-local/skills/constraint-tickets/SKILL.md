---
name: constraint-tickets
license: MIT
description: "Turn a feature request or change into one-constraint tickets built from the code's existing business rules, and generate the completion hook that refuses to let an agent finish until each checkable constraint holds. Use when asked for constraint tickets, to break this into tickets, one constraint per ticket, a stop hook, a completion hook, an agentStop hook, a gate, or to not let the agent finish until a constraint holds, or to make an agent respect rules a request never states."
---

# Constraint tickets and a completion hook

Outputs in the repository root: `CONSTRAINTS.md` (list and routing table), `tickets/NN-<slug>.txt` (one per ticket) and, when asked, the gate and hook from `references/hook-template.md`. Create `CONSTRAINTS.md` first and append as you go. Do not commit, push or install a hook unless asked.

## 1. Preflight

Call `status`, then `corpus_info`. Proceed only if `status.state` is `snapshot_selected`, the latest ingest has not `failed`, and the `sao:Rule` count is above zero. Otherwise say CoreStory evidence is unavailable, relay `status.next_step`, and ask whether to continue from source alone. Never call `init` or `ingest` without the user's explicit OK. If `search` says it "could not answer", use `rules_for`, `entity`, `connections` and `read_file`.

## 2. Build the constraint list from rules

A constraint is a fact the request never states but the change must respect. CoreStory v3 has no document generation; the list comes from rules.
1. Write the request and the business nouns and quantities it touches (amounts, counts, thresholds, dates, statuses).
2. `search(query, kind:"sao:Rule")` with two or more plain phrasings per noun, default limit. For each file the change will touch, `rules_for(path, start_line, end_line)`, following `next_call` until absent.
3. `entity(entity_id, include:["description","evidence"])` on each candidate, then `read_file` the evidence lines. Keep only rules whose quote or condition you saw. Include rules enforced in other layers (services, entities, config, SQL, UI). Hits are leads; `rules_for` also returns rules that only support the lines.
4. Write each as one statement: `C<n>: <constraint>; id; path:start-end; values`.

## 3. Route each constraint

Before calling one violated, check the quantifier: test it at the strength written, no stronger. "From X" does not say "only from X". Write `QUANTIFIER CHECK: constraint says "<verbatim>" (<quantifier or none>); claim tested: <claim>; comparison: <same strength | claim is stronger | claim is weaker>`. A claim stronger than the constraint is a different, nearby behavior, not a violation.

Then, in a table in `CONSTRAINTS.md`: constraint, satisfied today (yes, no, not checked), ticket file, assertion (how), block or flag.
- Violated today or newly required: a ticket.
- Checkable against a working tree (fixture, test on production paths, static predicate): an assertion in the gate. An already-true checkable constraint is an assertion only.
- Not the current ticket's job: flag (advisory), not block.
Whether the code satisfies a constraint is your reading of source, not a CoreStory finding; mark it as such.

## 4. Write the tickets

One constraint per ticket, as its own file. Rules that were measured on kenobi tickets:
- One constraint, the whole ticket: no "while you're there", no "see also".
- Name the area, never the site: no file paths, methods, line numbers or identifiers in the ticket text. The evidence stays in `CONSTRAINTS.md`.
- Symptom and consequence, then one checkable ask in the imperative. Investigation or "review" asks state no constraint.
- Plain business language, two to five sentences, standing alone.
Read `references/ticket-examples.md` after writing, as a register check.

## 5. Completion hook (when asked)

Follow `references/hook-template.md`: a harness-neutral gate script (exit 0 pass, 1 block, 3 tamper, 4 could not run; it owns the verdict and every error path blocks) and a binding per harness. The binding differs: Claude Code `Stop` blocks with exit 2 and a stderr message; Copilot CLI `agentStop` needs a JSON `{"decision":"block",...}` on stdout. Do not port one across. Install user-level, outside the repository the agent edits. The assertions, build command and fixture are the user's to write; offer a draft from the verified rules and values. Validate with the six checks in the template and then watch a real session get refused. Scope the blocking gate to the ticket in hand; flag the rest.

## What this does not claim

Sequencing (constraint tickets before the feature) is a hypothesis, unmeasured. The hook results in the template were measured on Copilot CLI with kenobi-generated specs, not CoreStory v3; the Claude Code binding is documented, not measured. A passing gate checks only its assertions, and CoreStory does not run code.

End `CONSTRAINTS.md` with `## Not verified`: rules not read back, areas not searched, constraints whose status is unchecked, and that CoreStory describes the ingested snapshot. Do not call the list complete.
