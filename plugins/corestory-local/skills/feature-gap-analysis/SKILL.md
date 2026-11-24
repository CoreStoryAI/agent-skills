---
name: feature-gap-analysis
license: MIT
description: "Work out what already exists, what is missing, which files change and in what order before building a feature, using CoreStory v3 rules and code evidence, and write the result to GAP-ANALYSIS.md. Use when asked what needs to change to build or add a feature, for a gap analysis, an impact analysis, or an implementation plan before coding."
---

# Feature gap analysis

> On hosted CoreStory the tools are prefixed `v3_` (e.g. `v3_rules_for`), take a `project_id` (from `list_projects`), and there is no `status`/`init`/`ingest`: start with `v3_corpus_info`. When following a `next_call`, use the `v3_` name and the same `project_id`.

Output: `GAP-ANALYSIS.md` in the repository root (or the file the user names). Create it first and append as you go. This skill plans; do not edit code, commit or push.

## 1. Preflight

Call `status` if available, then `corpus_info` (hosted: `v3_corpus_info` for the chosen project). Proceed only if `status.state` is `snapshot_selected`, the latest ingest has not `failed`, and the `sao:Rule` count is above zero. Otherwise say CoreStory evidence is unavailable, relay `status.next_step`, and ask whether to continue from source alone. Never call `init` or `ingest` without the user's explicit OK. If `search` says it "could not answer", use `rules_for`, `entity`, `connections` and `read_file`.

## 2. Feature

Write the requested feature, its inputs, outputs and acceptance behavior at the top of the file. Ask for missing details if you can; if not, record your assumptions.

## 3. What exists

- Rules about each concept the feature touches: `search(query, kind:"sao:Rule")` with two or more plain phrasings, then `entity(entity_id, include:["description","evidence"])`, then `read_file(path, start_line, end_line)`.
- Similar code and extension points: `search(query, kind:"plot:Chunk")`, then `read_file`. `list_files(prefix)` for the nearby tests, config and schema files.
- Callers and callees of the code to change: `connections(entity_id)` on a symbol or chunk's `plot:Content`; on COBOL, `entity(parsed_calls_id)` via `connections(content, predicates:["plot:hasparsedcalls/v1"])`.
- Existing features: capabilities and features are reachable only by `connections` from a rule up to the revision's `plot:feature_manifest/v1`, then `plot:has_capability/v1`. Use the related entity's `entity_id`, never the `edge_id`. Do not call `entity` on the manifest (about 135 KB). Rules are not linked to features, so match them by file path.

## 4. Gaps

For each file you plan to touch, `rules_for(path, start_line, end_line)` and follow `next_call` to the end; check each rule with `entity` and `read_file`. Then list gaps by category with ids: data model (DM-), business logic (BL-), UI (UI-), output (RO-), integration (IG-), constraints (CG-). For each: current state with `path:start-end`, required change, rules that stay in force, dependencies on other gaps. A rule enforced in more than one layer (service, schema, UI validator, COBOL, SQL) is a gap in every layer; list each site.

## 5. Plan

Dependency-ordered steps: data model, business logic, UI, output, integration. For each step, the files, the pattern to copy (cite a file), and the tests to add or run. Mark what could be deferred and the highest-risk change.

## 6. Not verified

End with `## Not verified`: rules not read back, categories with few or no hits (say so; `search` never returns empty), files not inspected, and that CoreStory describes the ingested snapshot, not necessarily the working tree. CoreStory does not run code, so every behavior claim is from reading.

Do not call the analysis complete.
