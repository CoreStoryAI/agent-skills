---
name: corestory-ask
license: MIT
description: "Compare a local CoreStory answer with repository evidence to identify intelligence gaps. Use to audit an answer, investigate a suspected gap, or generate evidence-backed gap candidates."
---

# Compare CoreStory with source

Use this skill for a deliberate differential, not routine development work.

Confirm the local graph with `corpus_info`.
Ask the selected CoreStory tools a focused question about the codebase.
Capture the returned claims, evidence locations, and snapshot limits.

Independently investigate the same question in the repository.
Search and read the relevant source without treating the graph answer as authoritative.
Cite path and location for every code-grounded claim.

Present the CoreStory finding, the source-grounded finding, and a concise delta table.
Classify each delta as one of the following:

- CoreStory gap: source evidence contradicts or materially exceeds the graph finding.
- CoreStory adds value: the graph found useful context that the source-only pass missed.
- Staleness: a source change is newer than the captured snapshot.
- Uncertain: the conflict cannot be resolved from available evidence.

Treat deltas as leads, not verdicts.
Offer a narrowly scoped gap report only for well-evidenced CoreStory gaps.
