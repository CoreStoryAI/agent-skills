---
name: implement-feature
license: MIT
description: "Implement a feature with local CoreStory evidence and test-driven development. Use for feature tickets, enhancements, or requested product changes, not defect investigation."
---

# Implement a feature

Confirm local graph availability with `corpus_info`.
If the workspace has not been ingested, say so plainly and continue only with source files the agent can inspect directly.

Extract the requested outcome and acceptance criteria.
Search for analogous behavior, extension points, data structures, tests, and integration boundaries.
Use entities and connections to identify the code path and dependencies.
Read the relevant source and existing tests before deciding where to change code.

Present a concise implementation boundary: files to modify or add, preserved invariants, and evidence for the chosen pattern.
Ask for clarification only when missing acceptance criteria materially affect the implementation.

Write tests for the requested behavior before production changes.
Verify that they fail for the missing behavior when possible.
Implement the smallest change that satisfies the criteria and follows local conventions.
Run the new tests and the relevant wider suite.

Report the behavior delivered, source evidence, changed files, commands run, and remaining risks.
Do not create a ticket, commit, or publish a change unless the user asks.
