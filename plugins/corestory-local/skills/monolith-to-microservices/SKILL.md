---
name: monolith-to-microservices
license: MIT
description: "Design the extraction of one service from a monolith using the strangler fig pattern: service boundary, database decomposition, and facade plan, written to modernization/05-extraction-WP.md. Use for service-boundary work, microservice extraction, or database decomposition for one approved work package."
---

# Monolith to microservices: one extraction

Output: `modernization/05-extraction-<wp>.md` where `<wp>` is the work package id (for example `WP-01`). Design only. Building the service is `implement-feature`, in its own session, one work package at a time.

## 1. Preflight and inputs

Call `status`, then `corpus_info`. Proceed only if `status.state` is `snapshot_selected`, the latest ingest has not `failed`, and the `sao:Rule` count is above zero; otherwise relay `status.next_step`. Never call `init` or `ingest` without the user's explicit OK.

Read `modernization/04-work-packages.md`, `03-target-architecture.md` and `02-rules-inventory.md`. All must be `approved`; if not, stop and name the file. Ask which work package to extract if the user did not say; take the package's BR ids from the file. Start the output file with the header:

```
---
phase: extraction-<wp>
status: draft
date: YYYY-MM-DD
snapshot: <id from corpus_info>
approver: pending
---
```

## 2. Service boundary

Classify each program, module and table in the package as MOVE, SHARE or LEAVE. Evidence: `connections(entity_id)` for callers and callees, `list_files(prefix)`, `read_file(path, start_line, end_line)`. Look for hidden coupling: direct calls, shared state, globals, implicit ordering, batch jobs that touch the same tables. For each package rule: `entity(entity_id, include:["description","evidence"])`, `read_file` the evidence, and say where it will live after the move. Hits are leads; cite only lines you read.

## 3. Database decomposition

Per table: owned, read-only, or shared writes, with the code that reads or writes it. Choose and justify one strategy (database per service, schema ownership as an intermediate step, change-data capture, or API-mediated access) and give the sync approach during coexistence and the rollback.

## 4. Facade and communication

List every entry point into the component (`search` plus `connections`), the routing facade (gateway or reverse proxy, or branch-by-abstraction in code), sync or async per interaction, and the anti-corruption layer where the old and new models differ.

## 5. Gate

Mark the first extraction as the pattern later ones follow. Stop. The engineering lead reviews boundary, data plan and facade, and approves through `code-modernization`. Do not start building in this session. When approved, the build uses `implement-feature` with this file as input and the Transform, Coexist, Eliminate order; verification uses `behavioral-verification`; cutover needs its own approval from the engineering lead.

End with `## Not verified`: edges and tables not read, circular dependencies unresolved, unpaged results, and that results describe the ingested snapshot. Leave `status: draft`.

Do not call the design complete. No claims of speed or reduced risk. CoreStory does not run code, so performance after extraction is untested.
