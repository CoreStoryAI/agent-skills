---
name: corestory-ask
license: MIT
description: "Check a CoreStory v3 answer against the source and write down where they differ. Use to audit what CoreStory says about a codebase, test whether it missed or misstated something, or collect evidence-backed gap candidates."
---

# Compare CoreStory with source

A deliberate differential, not routine development. Output: `ASK-DELTA.md` in the repository root (or the file the user names).

1. Preflight: `status`, then `corpus_info`. If the state is not `snapshot_selected`, the latest ingest `failed`, or the `sao:Rule` count is zero, stop and relay `status.next_step`. Never call `init` or `ingest` without the user's explicit OK.
2. Take the question (ask the user for one focused question if none). Record the CoreStory side: `search(query, kind:"sao:Rule")` and `kind:"plot:Chunk"` at default limits; `rules_for(path, start_line, end_line)` for files; `entity(entity_id, include:["description","evidence"])`; `connections` where relations matter. Write the claims, their ids and cited `path:start-end`. If `search` says "could not answer", use the other tools and say so.
3. Investigate independently: Grep and `read_file(path, start_line, end_line)` on the source. Do not treat a graph claim as true; cite only lines you read.
4. Write a delta table: claim, CoreStory evidence, source evidence, classification:
   - CoreStory gap: source contradicts or materially exceeds the graph.
   - CoreStory adds value: the graph found something the source pass missed.
   - Staleness: the working tree changed after the snapshot.
   - Uncertain: the evidence cannot settle it.
5. End with `## Not verified`: claims not re-read, paged results not followed. Deltas are leads, not verdicts. `search` never returns empty, so a missing rule in the results does not prove it is absent. Offer a narrow gap report only for well-evidenced gaps.
