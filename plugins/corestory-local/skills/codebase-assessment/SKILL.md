---
name: codebase-assessment
license: MIT
description: "Assess how ready a codebase is to modernize and what could go wrong, using CoreStory v3 rules, features, capabilities and call edges, and write the findings to ASSESSMENT.md. Use when asked to assess, size up, audit or evaluate a legacy system, its modernization readiness, risks, technical debt, or what is in it."
---

# Assess modernization readiness

Output: `ASSESSMENT.md` in the repository root (or the file the user names). Create it first with a header and append as you go. Do not create tickets, commits or pushes unless asked.

## 1. Preflight

Call `status`, then `corpus_info`. Proceed only if `status.state` is `snapshot_selected`, the latest ingest has not `failed`, and the `sao:Rule` count is above zero. Otherwise say CoreStory evidence is unavailable, relay `status.next_step`, and ask whether to continue from source alone. Never call `init` or `ingest` without the user's explicit OK; `ingest` spends their model-provider money. If `search` says it "could not answer", use `rules_for`, `entity`, `connections` and `read_file`.

## 2. Inventory

- Size: record the `corpus_info` counts (files, rules, symbols, features, capabilities, call sites, languages). Counts describe the snapshot, not completed ingestion.
- Layout: `list_files(prefix:"cobol/")` and similar for each top directory; to page, pass `next_cursor` back unchanged with the same `prefix` and `limit` (a cursor with a different prefix or limit is an error). Always pass a prefix and copy the cursor exactly; do not page a whole repository. Note languages, build and deploy files, tests, config, JCL, copybooks and SQL.
- Capabilities and features are not searchable. Reach them from any rule: `connections(rule_id)` to its `plot:Content`, `connections(content)` to its `plot:File`, `connections(file)` to the `plot:Revision`, `connections(revision, predicates:["plot:feature_manifest/v1"])`, then `connections(manifest, predicates:["plot:has_capability/v1"])`. Use the related entity's `entity_id`, never the `edge_id`. Never call `entity` on the manifest (about 135 KB). Open each capability with `entity(capability_id)` for its summary and features; `entity(feature_id, include:["description"])` gives the summary and cited symbols. If no manifest exists, say the codebase has no feature map.

## 3. Rules and risk

- By theme, `search(query, kind:"sao:Rule")` with plain phrasings: validation, money and rates, limits, authorization, state transitions, scheduling, error handling, hardcoded values. Rules carry no category field, so you assign the theme. Default limit; hits are leads and `search` never returns empty.
- Open the ones that matter with `entity(entity_id, include:["description","evidence"])` and read the lines with `read_file(path, start_line, end_line)` before citing.
- Concentration: use `rules_for(path)` (follow `next_call`) on the largest or most central files to see where logic sits.
- Coupling: the same value or rule appearing in several layers or languages is a risk; record each site. Where call edges exist (COBOL), do this for at least the largest programs: `connections(content_id, predicates:["plot:hasparsedcalls/v1"])` then `entity(parsed_calls_id)` lists callers and callees by name; use it for hubs and call chains. Java and Python have no call sites in this release.
- Source scan: anything CoreStory cannot see (dependency versions, secrets, tests, CI) you check with Grep and `read_file`, and label as source-only.

## 4. Write the report

Sections: Summary, Inventory, Capabilities, Rules by theme (with `path:start-end`), Hubs and coupling, Risks (severity, evidence), Readiness by area (low, medium, high, with reasons), Suggested order of work, Not verified.

## 5. Not verified

End with `## Not verified`: rules not read back, themes not searched, areas with no structure (languages without a grammar), paged results not followed, and that CoreStory describes the ingested snapshot, not necessarily the working tree. CoreStory does not run code, so runtime behavior, performance and test coverage are unassessed.

Do not call the report complete or the scores exact.
