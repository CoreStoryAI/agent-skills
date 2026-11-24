---
name: ma-technical-due-diligence
license: MIT
description: "Review an acquisition target's codebase for technical risk with CoreStory v3 evidence and write the findings to DILIGENCE.md. Use when asked for technical due diligence, an acquisition or M&A review, a code quality, security, scalability or integration risk review, or what to worry about in a codebase before buying it."
---

# Technical due diligence

> On hosted CoreStory the tools are prefixed `v3_` (e.g. `v3_rules_for`), take a `project_id` (from `list_projects`), and there is no `status`/`init`/`ingest`: start with `v3_corpus_info`. When following a `next_call`, use the `v3_` name and the same `project_id`.

Output: `DILIGENCE.md` in the repository root (or the file the user names). Create it first and append findings as you go. Do not create tickets, commits or pushes unless asked.

## 1. Preflight

Call `status` if available, then `corpus_info` (hosted: `v3_corpus_info` for the chosen project). Proceed only if `status.state` is `snapshot_selected`, the latest ingest has not `failed`, and the `sao:Rule` count is above zero. Otherwise say CoreStory evidence is unavailable, relay `status.next_step`, and ask whether to continue from source alone. Never call `init` or `ingest` without the user's explicit OK. If `search` says it "could not answer", use `rules_for`, `entity`, `connections` and `read_file`.

## 2. Orient

Record the `corpus_info` counts and languages. Do the capability walk below and open each capability with `entity`. `list_files(prefix)` (page with `next_cursor`, unchanged, same prefix and limit) for the layout, build, deploy, CI and test files. Capabilities: from any rule, `connections` up to its `plot:Content`, `plot:File`, `plot:Revision`, then `plot:feature_manifest/v1`, then `plot:has_capability/v1`. Use the related entity's `entity_id`, never the `edge_id`. Never call `entity` on the manifest (about 135 KB). `entity(capability_id)` gives summaries. Say so if there is no feature map.

## 3. Risk domains

Run `search` on every domain below (not Grep alone; Grep covers only what CoreStory cannot see). One finding per entry: statement, severity, evidence `path:start-end`, source (CoreStory rule, source-only). Use `search(query, kind:"sao:Rule")` with plain phrasings, `entity(entity_id, include:["description","evidence"])`, and `read_file(path, start_line, end_line)`. Hits are leads; `search` never returns empty.

- Money, rates and limits: where amounts are computed and rounded, hardcoded rates and thresholds, rules duplicated across layers or languages.
- Access and secrets: authorization checks, auth flow, credentials or tokens in code or config (Grep, then `read_file`).
- Personal data: where customer or account data is stored, logged, exported or deleted.
- Integrations: external calls, files and queues, batch jobs and their ordering; on COBOL, call edges through `connections(content_id, predicates:["plot:hasparsedcalls/v1"])` then `entity(parsed_calls_id)`.
- Maintainability: concentration of rules in a few files (`rules_for(path)`), duplicated logic, dead or unreferenced code, tests and CI present (`list_files`).
- Dependencies and licenses: read manifests and lock files directly; CoreStory does not index CVEs or license data. Label as source-only.

## 4. Validate

Before a finding goes in the report, `read_file` the cited lines and confirm. Mark the rest "unverified". Separate real production values from fixtures and placeholders.

## 5. Report

Sections: Summary (top findings for deal risk), Architecture and capabilities, Critical risks, Technical debt, Integration effort, Recommendations, Not verified. Give no valuation, dollar or effort figures you cannot support.

End with `## Not verified`: rules not read back, domains not searched, languages without structure, paged results not followed, dependency and license checks not done, and that CoreStory describes the ingested snapshot, not necessarily the working tree. CoreStory does not run code; security and performance are read, not tested.

Do not call the review complete or the target safe.
