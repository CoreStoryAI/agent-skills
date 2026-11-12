---
name: bug-resolver
license: MIT
description: "Investigate and fix defects with local CoreStory evidence and test-driven development. Use for bug reports, regressions, failures, root-cause investigations, or bug-ticket IDs."
---

# Resolve a bug

Use `corpus_info` to confirm that the local codebase is available.
If it is unavailable, explain that CoreStory must be run against an ingested workspace before it can provide graph evidence.

Extract the symptom, expected behavior, affected scope, and reproduction conditions from the request or ticket.
Search for the affected behavior, related symbols, callers, tests, and error paths.
Use entities and connections to trace the smallest relevant execution path.
Read source around every candidate finding before making a claim.

State the leading hypothesis, its source evidence, and credible alternatives.
Write a regression test that fails against the current behavior before changing production code.
Implement the smallest change that restores the intended behavior.
Run the regression test and the relevant wider test suite.

Report the root cause, changed files, remaining uncertainty, and commands actually run.
Do not create a ticket, commit, or publish a change unless the user asks.
