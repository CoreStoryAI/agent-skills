---
name: behavioral-verification
license: MIT
description: "Compare a modernized component against the approved business rules inventory by reading legacy source and new code, classify each rule, and recommend tests; writes modernization/06-verification-COMPONENT.md. Use for behavioral equivalence, rule-by-rule comparison, or an equivalence report. It compares code; it does not run it."
---

# Behavioral verification (static comparison)

Output: `modernization/06-verification-COMPONENT.md`. This is a source-to-source comparison. CoreStory does not run or test code, and neither does this skill: it recommends the tests that would settle what reading cannot.

## 1. Preflight and inputs

Call `status`, then `corpus_info`. Proceed only if `status.state` is `snapshot_selected`, the latest ingest has not `failed`, and the `sao:Rule` count is above zero; otherwise relay `status.next_step`. Never call `init` or `ingest` without the user's explicit OK. The ingested snapshot is the legacy system; the modernized code is read from the working tree unless it was ingested too.

Read `modernization/02-rules-inventory.md` (must be `approved`) and, if present, `04-work-packages.md` or `05-extraction-*.md` for the component's scope. Ask for the component name and where the modernized code lives if not given. If the inventory is missing or `draft`, stop and name it. Do not verify code written in this session; ask for a fresh session.

Start the file:

```
---
phase: verification-<component>
status: draft
date: YYYY-MM-DD
snapshot: <id from corpus_info>
approver: pending
---
```

## 2. Rule by rule

For each inventory rule in scope (list the BR ids first; scope narrow rather than sampling silently):

1. Legacy: `entity(entity_id, include:["description","evidence"])` if the rule has a CoreStory id, then `read_file(path, start_line, end_line)` on the evidence. Confirm the condition, values and violation behavior. If the inventory and source disagree, source wins; note it.
2. Modernized: find the implementation with `search`, `list_files` or by opening the new code directly. Read it. Compare conditions, literals, rounding, ordering, side effects, error behavior, output.
3. Classify exactly one: `Equivalent`, `Improved`, `Different`, `Missing`, or `Unverified` (reading cannot settle it; say what is needed). Never call a rule Equivalent on a name match alone; cite `path:start-end` for both sides.
4. Flag ambiguous legacy behavior for a domain expert. Do not assume it is a bug.

## 3. Beyond listed rules

For each in-scope legacy file read, `rules_for(path, start_line, end_line)` (follow `next_call`) and note rules not in the inventory that the new code also omits. Compare integration points: API contracts, data formats, dates, precision, nulls, consumers. List boundary cases (null, limits, rounding, temporal edges) the rules imply.

## 4. Report and gate

Table: BR id, legacy cite, new cite, classification, notes. Then differences (improvement, deviation, regression), missing rules with a recommended action, and a recommendation: Ready for the Eliminate step, Needs remediation, or Needs review. Then `## Recommended tests`: characterization or golden-master inputs, shadow comparison points, data reconciliation checks, each tied to a BR id. These are recommendations; say none was run. Stop. A domain expert or engineering lead validates before legacy code is retired. Leave `status: draft`.

End with `## Not verified`: rules not read on both sides, files not reached, unpaged results, and that CoreStory describes the ingested snapshot.

Do not say behavior was verified at runtime. Do not call the comparison complete.
