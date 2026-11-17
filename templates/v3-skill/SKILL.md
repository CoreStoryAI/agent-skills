---
name: example-skill
license: MIT
description: "One sentence on what it produces. One sentence on when to use it."
---

# Title

Preflight: call `status`, then `corpus_info`. If the state is not `snapshot_selected`, the latest ingest `failed`, or the `sao:Rule` count is zero, stop and relay `status.next_step`. Never call `init` or `ingest` without the user's explicit OK.

Scope: restate the task's scope in one line. If it is broad and you can ask, ask; if you cannot ask, take the narrowest reading and record it.

Find: `search(query, kind:"sao:Rule")` for concepts; `rules_for(path, start_line, end_line)` for files, following `next_call`. Use default limits.

Inspect: `entity(entity_id, include:["description","evidence"])`.

Verify: `read_file(path, start_line, end_line)` on the cited lines before any claim. Hits are leads.

Write: `<OUTPUT>.md` in the repository, started early and appended as you go. Cite `path:start-end`. End with "Not verified".

Do not claim CoreStory ran or tested anything. Do not call the result complete.
