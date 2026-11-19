---
name: using-corestory
license: MIT
description: "Answer questions about a codebase with CoreStory v3, citing source lines you checked. Use when asked how something works, where a rule or value comes from, what a file enforces, or to trace or explain code in a repository CoreStory has ingested."
---

# Using CoreStory v3 tools

The server instructions list the tools. This is the short recipe for answering a question with evidence.

1. Preflight: `status`, then `corpus_info`. Proceed on `state: snapshot_selected`, a latest ingest that has not `failed`, and a nonzero `sao:Rule` count. Otherwise relay `status.next_step` and ask whether to continue from source alone. Never call `init` or `ingest` without the user's explicit OK; `ingest` spends their model-provider money. If `search` says it "could not answer", use `rules_for`, `entity`, `connections` and `read_file`.
2. Rules about a concept: `search(query, kind:"sao:Rule")`; the excerpt is the rule statement. For code, `kind:"plot:Chunk"`.
3. Rules for a file or lines: `rules_for(path, start_line, end_line)`; follow `next_call` to the end. It also returns rules that only support those lines.
4. Detail: `entity(entity_id, include:["description","evidence"])` gives the statement, values and the quote. A plain `entity` call returns almost nothing for a rule.
5. Verify: `read_file(path, start_line, end_line)` on the cited lines before you state the rule. Cite `path:start-end` only for lines you read.
6. Structure: `connections(entity_id)` for edges; `list_files(prefix)` for layout. Features and capabilities are reachable only through `connections`, and rules are not linked to features.

Hits are leads: `search` never returns an empty result, so a nonsense query still gets five hits. An empty or exhausted result does not prove no rule exists. Keep default limits and follow `next_call` or `next_cursor`; never use `limit:100` on `search` (100 to 150 KB). Read line ranges, not whole files.

Say what you could not verify. CoreStory describes the ingested snapshot, not necessarily the working tree, and it reads code; it does not run it. Do not call an answer complete.
