---
name: business-rules-extraction
license: MIT
description: "Extract and source-verify business rules from a local CoreStory graph and repository source. Use for validation, authorization, state-transition, invariant, or implicit-rule discovery."
---

# Extract business rules

Confirm graph availability with `corpus_info`.
Agree on a bounded domain or module when the requested scope is broad.
Search for the business concept, related entities, state changes, validation, authorization, persistence, and tests.
Use entity and connection results to trace the relevant flows.
Read source around every candidate rule.

For each rule, record the claim, source location, enforcement point, violation behavior, scope, and confidence.
Do not call a declaration an enforced rule until source shows the check that rejects invalid input or prevents an unauthorized action.
Classify rules as confirmed, corrected, declared-but-not-enforced, or uncertain.

Trace critical flows from entry point to side effects to find behavior that a domain search misses.
Look for ignored input, overwrites, swallowed errors, UI-only checks, and dead fields.

Deliver a compact rules inventory grouped by domain, with evidence locations and a separate list of declarations that are not enforced.
State what could not be verified from the captured source.
