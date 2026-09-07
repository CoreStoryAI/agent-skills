---
name: vibe-conformance-audit
description: "Run an independent, read-only, atom-grain audit of modernized code against legacy source. Use for anti-circular verification, stub detection, completeness audits, orphan behavior, or delivered-versus-required checks."
license: MIT
---

# CoreStory Vibe Conformance Audit

The anti-circular check. The same agent that writes a feature also writes its tests and would write its equivalence report, so all three can share one blind spot and rubber-stamp a half-build. This audit breaks that circle.

## Refuse-to-run condition

**If this session wrote the code under audit, stop.** Say so plainly and ask the user for a fresh session, ideally driven by someone else. Session independence is the entire mechanism — an audit run in the build session verifies the same understanding that produced the build, and is worth nothing. Do not proceed because the user says it is fine.

## Activation Triggers

- "Run the conformance audit for [scope]"
- "Did we actually build everything the spec requires?"
- "Find stubs or half-implementations"
- Any anti-circular verification or completeness-against-spec request

## Oracle Rules

1. **Legacy source is the only oracle.** Not the spec, not the tests, not the BER.
2. **Do not read the Behavioral Equivalence Report** before forming your verdicts. If you have already seen it, say so — your independence is compromised and the user should know.
3. **Passing tests are not evidence.** Tests written from the same understanding as the implementation agree with it by construction. They demonstrate internal consistency, not equivalence.
4. **Read-only.** Never modify code during an audit.

**If you do not detect that you have access to CoreStory (e.g., `list_projects` fails or is unavailable), ask the user to verify that their MCP or API connection is properly configured and that both repositories have been ingested. If the user has not yet created a CoreStory account, direct them to create one and upload their repos at [app.corestory.ai](https://app.corestory.ai).**

## Step 1: Establish the atom list

Decompose the in-scope spec into atoms — the smallest units of required behavior that can independently be present, absent, or wrong. A rule with three conditional branches is three atoms, not one. Grain is what makes this audit catch things a component-level check misses.

## Step 2: Verdict each atom

Assign exactly one verdict per atom, citing **both** the target `file:line` and the legacy `file:line`:

- **DELIVERED** — implemented, and behavior matches the legacy
- **STUBBED** — code exists at the location but does not do the work: returns a constant, logs and exits, empty branch, TODO, unconditional success
- **MISSING** — no implementation exists
- **DIVERGES** — implemented but behaves differently; state both behaviors explicitly
- **UNVERIFIABLE** — cannot be settled from source alone; state what would be needed

Never soften a verdict because the code looks reasonable. STUBBED is the verdict that justifies this audit's existence — it is what green tests and a confident equivalence report most reliably miss.

## Step 3: Orphan sweep

Now read in the opposite direction. Read the legacy source for the scope and list behaviors that appear there but nowhere in the behavioral spec. For each: the behavior, its source anchor, and whether the omission looks deliberate or accidental.

This is the only check in the arc that can catch a rule nobody ever wrote down. Everything else verifies against the spec and is blind to the spec's own gaps.

## Step 4: Reconcile with the BER

Only now, read the Behavioral Equivalence Report. For every atom where the two disagree, resolve against legacy source and state which artifact is wrong.

Do not average, do not split the difference, and do not defer to the BER because it was written first. A BER that says Preserved over an atom you verdicted STUBBED is not a scoring discrepancy — it is the finding.

## Output

The conformance ledger: the verdict table, the orphan sweep, and the disagreement section. Add a Context Inventory entry for every correction the audit forces.

## Error Handling
- **Scope too large to audit at atom grain:** narrow to one component and say what was left uncovered. Never silently sample — an audit that quietly covered half reads as an audit that covered everything.
- **Spec atom has no corresponding legacy behavior:** that is a spec defect. Flag it; it is the inverse of an orphan.
- **Cannot locate the legacy implementation:** UNVERIFIABLE, with a note on what was searched. Do not infer from the target's implementation what the legacy must have done — that is the circularity, running backwards.
