# House style for CoreStory v3 skills

Applies to skills in `plugins/corestory-local`. Written against the CoreStory release `2026.11.17` (CLI 0.1.0-alpha.1, MCP guidance v2). The tool surface will change; re-check names against `tools/list` before each release.

## Why the skills are short

Measured on earlier builds: extra correct text has made agent results worse, Claude Code cuts MCP instructions at 2,048 characters and skill descriptions at 1,536, and an agent only reaches CoreStory when its first tool call is a CoreStory call. So a skill is a recipe of named tool calls plus a file to write. It does not re-teach the server's instructions. Target: a SKILL.md body under about 70 lines.

## The tools

Ten, over stdio: `status`, `init`, `ingest` (lifecycle); `corpus_info`, `search`, `entity`, `connections`, `read_file`, `list_files`, `rules_for` (exploration). Skills name the tools they use. They never name a tool that is not in this list.

## Rules of the house

1. **Preflight first.** Call `status`, then `corpus_info`.
   - `state: snapshot_selected` with a latest ingest that is not `failed`, and a nonzero `sao:Rule` count: proceed.
   - `uninitialized`, `initialized` (no snapshot), or a `failed` latest ingest: stop and tell the user what `status.next_step` says. Do not substitute source-only work silently; say that CoreStory evidence is unavailable and ask whether to continue without it.
   - Never call `init` or `ingest` without the user's explicit OK in this conversation. `ingest` spends the user's model-provider money, blocks until done, and asks for no consent itself. `init` needs the user's own telemetry choice.
   - If `search` fails with "could not answer", the embedding key is missing. `rules_for`, `entity`, `connections` and `read_file` still work; say so and continue with those.
2. **Two lookup recipes.** Use these shapes instead of inventing new ones.
   - *Rules for the file I am editing:* `rules_for(path, start_line, end_line)`, follow `next_call` until it is absent, then `entity(entity_id, include:["description","evidence"])` for the rules that matter, then `read_file(path, start_line, end_line)`.
   - *Rules about concept X:* `search(query, kind:"sao:Rule")` (the excerpt is the rule statement), then `entity(... include:["description","evidence"])` for values and the verbatim quote, then `read_file`.
3. **Verify before you cite.** A rule from the graph is a lead. Before it goes into an output, `read_file` the evidence lines and confirm the quote or condition is there. Cite `path:start-end` only for lines you read or the tool returned. Mark the rest unverified.
4. **Hits are leads.** `search` never returns empty; a nonsense query returns five hits. `rules_for` also returns rules that only support the lines asked about. An empty or exhausted result does not prove no rule exists. A first page is not the full list.
5. **Keep calls small.** Use default limits. Follow `next_call` rather than raising `limit`; never use `limit=100` on `search` (100–150 KB responses). Read line ranges, not whole files.
6. **Outputs go to files in the repo,** not conversation state. Create the file early with its header and append as you go. Name it in the skill. A finished file is the deliverable; a chat summary is not.
7. **Say what you could not verify.** Every output file ends with a "Not verified" section: rules not read back against source, areas not searched, languages without structure, truncated or unpaged results.
8. **The snapshot is not the working tree.** Results describe the ingested snapshot. Say so if the user may have edited files since.

## Claims guardrails (binding on skill text and on what skills tell users)

- Say "CoreStory v3" or "CoreStory", not the internal codename.
- Do not write "complete", "comprehensive", "ensures", "guarantees", or "exhaustive" about a result.
- CoreStory reads and indexes code. It does not run, test, or execute behavior. A skill may tell the agent to run tests; it may not say CoreStory verified runtime behavior.
- No Java, PHP, C# or SQL parsing claims beyond what a measured release note supports; no scale, speed or history claims.

## Frontmatter and packaging

Keep the existing conventions: `name` (matches the directory), `description` (under 1,024 characters, no angle brackets, says what and when), `license: MIT`, and nothing else in the frontmatter. Each skill keeps `agents/openai.yaml` with `$name` in `default_prompt`. `scripts/validate-release.py` enforces this.

## Skeleton

`templates/v3-skill/SKILL.md`.
