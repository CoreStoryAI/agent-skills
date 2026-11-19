---
name: corestory-reference
license: MIT
description: "Install CoreStory v3, set it up, and learn what its tools do and where they fall short. Use when asked how to install or start CoreStory, what the corestory tools are, why a CoreStory call failed or looks empty, or how to ingest a repository."
---

# CoreStory v3 reference

## Install and set up

- Install the CLI from get.corestory.ai and follow that page. Check with `corestory --version`.
- `corestory setup` is run by the user, never by you. It accepts the terms, records the telemetry choice and configures model keys on this machine. Ask them to run it in their own terminal.
- `corestory init` creates the local store in the repository directory; the MCP `init` tool needs the user's own telemetry answer. `corestory ingest` (or the MCP `ingest` tool) builds the graph. It calls the user's model provider and can cost money, it blocks until finished and asks for no consent itself. Run `init` or `ingest` only after the user says yes in this conversation, naming the cost. Prefer that they run `corestory ingest` themselves.
- `corestory mcp`, started from the repository folder, serves the tools over stdio. If `status` shows `uninitialized` or no snapshot, relay `status.next_step` and stop.

## The ten tools

- `status`: setup state, selected snapshot, latest ingest and its failure reason. Call first.
- `init`: create the local store (needs `telemetry_enabled` from the user).
- `ingest`: build the graph from the current files; paid; blocks.
- `corpus_info`: entity counts by kind. Counts do not prove ingestion completed.
- `search`: semantic search over `sao:Rule` and `plot:Chunk`; needs the embedding key.
- `entity`: one entity by exact id; add `include:["description","evidence"]` for rules.
- `connections`: edges of an entity, paged by `cursor`; the only route to features and capabilities.
- `read_file`: captured source by path and line range, lines numbered.
- `list_files`: captured paths by prefix, paged by `cursor`.
- `rules_for`: rules with evidence in a file or line range, paged by `next_call`.

## Known limits

- No relevance floor: `search` always returns hits, even for nonsense. Treat hits as leads.
- Sizes: `search` at `limit:100` is 100 to 150 KB; `read_file` of a large file is large; `entity` on a feature manifest is about 135 KB. Use defaults and line ranges.
- `rules_for` also returns rules that only support the lines; rules carry no category; rules are not linked to features.
- The snapshot is not the working tree. A copied or renamed repository directory reads as uninitialized, so run `status` after moving one.
- A failed or partial ingest can leave a store that looks usable; check `status.latest_ingest`. A missing embedding key makes only `search` fail ("could not answer").
- CoreStory reads and indexes code. It does not run or test it.

For tasks, use the specific skills: `business-rules-extraction`, `bug-resolver`, `implement-feature`, `codebase-assessment`, `feature-gap-analysis`, `ma-technical-due-diligence`, `using-corestory`.
