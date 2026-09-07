# Completion hook template — GitHub Copilot CLI

Everything here was measured on Copilot CLI 1.0.80–1.0.82 (Aug–Sep 2026). Re-verify the behaviors in
the last section on the build you are running; the CLI auto-updates, and it changed under two of the
measurements behind this file while they were still running.

This template is a shape, not a finished gate. It gives the hooks contract, the step order, the
fail-closed discipline, the `agentStop` script, and the validation rows. The assertion, the build
command, the classpath, the JDK pin, and the fixture are yours to write for your repository.

## 1. The hooks file

User-level, outside any repository, so the agent cannot read or delete it:
`$COPILOT_HOME/hooks/<name>.json`, where `COPILOT_HOME` is the directory Copilot CLI reads its
configuration from (default `~/.copilot`). Repository-level `.github/hooks/` also works
interactively, but in `-p` (non-interactive) mode it is **silently skipped** unless
`GITHUB_COPILOT_PROMPT_MODE_REPO_HOOKS=true` is set — and it sits inside the tree the agent edits.

```json
{
  "version": 1,
  "hooks": {
    "preToolUse": [
      { "type": "command",
        "matcher": "create|edit|str_replace|str_replace_editor|apply_patch|write|bash",
        "bash": "exec /abs/path/gate/hooks/tripwire.sh",
        "timeoutSec": 15 }
    ],
    "agentStop": [
      { "type": "command",
        "bash": "exec /abs/path/gate/hooks/agentstop.sh",
        "timeoutSec": 300 }
    ]
  }
}
```

- `agentStop` is where the refusal happens. `preToolUse` (the tripwire) denies edits to the gate's
  own files: `{"permissionDecision":"deny","reason":"..."}` — the write never happens and the reason
  reaches the model verbatim.
- For **flag mode** (surface, don't refuse), replace `agentStop` with a `postToolUse` hook that
  appends the advisory to the tool result via `modifiedResult`. The documented `additionalContext`
  field was **not implemented** on 1.0.80 — the hook fires, the JSON is accepted, nothing reaches the
  model. Use `modifiedResult`. This template ships no flag-mode script.

## 2. The `agentStop` script — fail closed

```bash
#!/usr/bin/env bash
# agentstop.sh — reads the agentStop payload on stdin, runs the gate, blocks on any non-zero exit.
# FAIL CLOSED: a hook that errors, times out, or writes nothing to stdout does NOT block — the CLI
# ends the turn and tells the model nothing. Every path out of here emits a block unless the gate
# positively returned 0.
set -uo pipefail
export PATH="/usr/local/bin:/opt/homebrew/bin:$PATH"   # a CLI-launched hook inherits no login shell
IN="$(cat)"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GATE="$HERE/../gate.sh"
GATE_WORK="${GATE_WORK:-$HOME/.corestory-gate}"       # same default the gate uses; export both absolutely

block() {
  printf '%s' "$1" | python3 -c 'import json,sys; print(json.dumps({"decision":"block","reason":sys.stdin.read().rstrip()}))' \
    || printf '{"decision":"block","reason":"GATE COULD NOT FORMAT ITS MESSAGE. Nothing was verified. Blocking."}\n'
  exit 0
}
field() { printf '%s' "$IN" | python3 -c "import json,sys; print(json.load(sys.stdin).get('$1','') or '')" 2>/dev/null; }

TREE="${COPILOT_PROJECT_DIR:-}"; [ -n "$TREE" ] || TREE="$(field cwd)"; [ -n "$TREE" ] || TREE="$PWD"
[ -d "$TREE" ] || block "GATE COULD NOT EXECUTE — no working tree to judge. Nothing was verified. Blocking rather than passing an unverified change."
[ -r "$GATE" ] || block "GATE COULD NOT EXECUTE — gate script missing at $GATE. Nothing was verified. Blocking."

OUT="$(bash "$GATE" --tree "$TREE" 2>/dev/null)"; RC=$?
[ "$RC" = 0 ] && exit 0                       # the ONLY path that lets the turn end
[ -n "$OUT" ] || OUT="GATE COULD NOT EXECUTE — the gate exited $RC without a message. Nothing was verified. Blocking."

# The CLI honours exactly 8 consecutive blocks; the 9th is discarded and the session ends rc=0 with
# no diagnostic. Count per session so the last honoured refusal says so.
SID="$(field sessionId)"; [ -n "$SID" ] || SID="nosession"
CNT_FILE="$GATE_WORK/blocks.$SID"; mkdir -p "$(dirname "$CNT_FILE")"
N=$(( $(cat "$CNT_FILE" 2>/dev/null || echo 0) + 1 )); echo "$N" > "$CNT_FILE"
[ "$N" -ge 8 ] && OUT="$OUT

This is the last refusal this session will honour. Fix the behaviour now or hand the ticket back."
block "$OUT"
```

**Sandboxed HOME trap.** If the harness that launches Copilot sandboxes `HOME`, the hook inherits
that environment and every `$HOME`-relative path (gate work dir, reference repo) resolves into an
empty directory. The gate takes its "cannot run" path — which is why that path must block, not pass.
Export the gate's paths absolutely (`GATE_WORK`, `GATE_REPO`) before launching, and pin the baseline
commit the pristine worktree is created from.

## 3. The gate script — contract

```
gate.sh [--tree DIR]
  exit 0   PASS      every assertion holds — or the tree is out of scope (a user-level hook fires everywhere)
  exit 1   BLOCK     an assertion failed; stdout is the message the agent will read
  exit 3   BLOCK     the gate's own files no longer match its manifest (tamper)
  exit 4   BLOCK     the change does not build, or the gate could not run
```

What it does, in order — and each step is a place a gate has silently lied before:

1. **Integrity first.** `shasum -a 256 -c MANIFEST` over the gate's own scripts and fixture. A
   neutralised gate must not be able to pass itself. The manifest cannot list itself; keep a copy of
   its hash outside the gate directory if you need to detect a regenerated manifest.
2. **Scope.** If the tree does not contain the project's marker file — pick one specific to this
   repository, such as its root build file plus a named module directory — exit 0. Never judge someone
   else's repository. Too broad a marker fires the hook in every repository of that language; too
   narrow, and a refactor silently takes the gate out of scope.
3. **Capture, don't trust.** Diff the live tree against `HEAD` under a throwaway `GIT_INDEX_FILE` so
   the gate does not touch the agent's index, apply the patch to a **pristine worktree outside the
   agent's directory**, and build there. Exclude the agent's own instruction files (`AGENTS.md`,
   `SPEC.md`, `.github/instructions/`) from what is judged. Never run the agent's tests — they assert
   the world in which the agent's bug cannot exist (two PR test files mocked the gateway into
   returning the correct type that production stamps wrong).
4. **Run the fixture** you wrote, against production code paths, and read the values it prints.
   **The gate script owns the verdict.** The fixture prints values — usually as JSON — and may always
   exit 0. Never derive the gate's exit code from the fixture's exit code: a gate that does so never
   blocks, and still passes three of the four original validation rows below. Carry the expected
   values in the gate itself; if the fixture prints its own `expect_*` fields and the gate reads them
   back, editing one constant makes the gate pass.
5. **The message is the product.** Name the file, the scenario, the observed and expected values, and
   the constraint in one sentence. Write a distinct message for every way of satisfying the number
   without fixing the behavior (see the Goodhart row below). End with: *"The gate ran its own fixture
   against your working tree in a worktree you do not control. It does not run the tests in this
   change. Make the behaviour correct, not the test."* On any could-not-run path, say instead that
   nothing was verified. A refusal carrying only the numbers converged nearly as often as one carrying
   the explanation; carry both.

## 4. Validate both ways before arming — record all six

| check | expected | what it protects against |
|---|---|---|
| the unmodified tree | **BLOCK** | a gate that cannot fail measures nothing |
| a known-good fix applied | **PASS** | a gate that cannot pass refuses correct work. The first pass of one measured gate blocked all fifteen diffs in a batch, including the only one that had actually repaired the site; the fix was a parsing defect in the gate, not in the diff. |
| a directory that is not this project | PASS (out of scope) | a user-level hook fires in every session on the machine |
| the fixture renamed or edited | **TAMPER** block | the agent, or a script, neutralising the check |
| the reference repository pointed at a nonexistent path | **BLOCK**, message says nothing was verified | a gate whose error handling exits 0 — the flag-mode pattern, right for an advisory, wrong for a gate |
| a wrong fix that reaches the expected number by breaking the case that was already correct | **BLOCK**, with its own message | an assertion that can be satisfied by moving the defect rather than fixing it — e.g., reaching the right tax on a discounted order by changing what every undiscounted order is charged, or by deleting the discount |

Then, if a fixture computes more than it asserts, **assert everything it computes that matters.**
The first version of one measured gate computed the refund ceiling for the ordinary case, printed it
in its JSON on every run, and never asserted on it — and passed a diff that refused the customer
30.00 of the 70.00 they were owed. Both directions have happened: a gate that blocked the correct fix
and a gate that passed a wrong one. Validate for both.

Two more things the measured gates do that this template only names: a lock with a staleness break,
because the CLI terminates hooks and leaves locks behind; and an append-only audit log, one row per
run, so a sweep leaves a record of what the gate decided.

## 5. Copilot CLI behaviors measured (re-verify on your build)

- `agentStop` + `{"decision":"block","reason":…}` → the turn does not end; `reason` is re-enqueued
  as the agent's next user message and it keeps working.
- A **bare non-zero exit** from an `agentStop` hook does **not** block. The model is told nothing.
- Hook **timeouts fail open**, silently. Set `timeoutSec` well above the gate's worst case (a 300 s
  budget against a 6–9 s gate with a warm worktree and cached classpath, 16.6 s cold; a gate built
  without those caches measured about 14.5 s).
- The CLI honours **8 consecutive blocks**; the 9th is discarded, the session ends `rc=0`, empty stderr.
- `preToolUse` + `{"permissionDecision":"deny","reason":…}` → the write never happens; the reason
  reaches the model verbatim.
- `postToolUse` `modifiedResult` works (text reaches the model, tool call still succeeds);
  `additionalContext` did nothing on 1.0.80.
- Repo-level `.github/hooks/*.json` are skipped in `-p` mode unless
  `GITHUB_COPILOT_PROMPT_MODE_REPO_HOOKS=true`.
- **Scope the blocking gate to the ticket it was written for.** Armed against a ticket that is not
  its own, it refuses every turn over pre-existing defects the agent did not cause — use flag mode.
- **The result to quote for the hook is 1 of 15 to 15 of 15 on the gate's assertion**, same ticket,
  same model. That 15 of 15 is entailed by construction — a gate pass implies the criterion passes —
  and the broader hazard-addressed measure was 12 of 15 with the gate against 13 of 15 without it.
  Never quote it as 15 of 15 correct code.
