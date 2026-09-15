# Completion hook template

This template is a shape, not a finished gate. It gives the gate contract, the step order, the
fail-closed discipline, the binding scripts, and the validation rows. The assertion, the build
command, the classpath, the JDK pin, and the fixture are yours to write for your repository.

**Two layers, and only one of them is harness-specific.**

| layer | what it is | portable? |
|---|---|---|
| **The gate** (§3) | a plain executable: exit `0` pass · `1` block · `3` tamper · `4` could not run | **yes** — it is a script with an exit code and cares about no harness |
| **The binding** (§1, §2, §2b) | ~15 lines wiring the gate to the harness's completion event | **no** — see below |

Write the gate once. Then take the binding for the harness you are arming.

**The bindings are close to inverses, so never port one across unchanged.** On Copilot CLI a bare
non-zero exit blocks *nothing* — the turn ends and the model is told nothing — and you must emit
`{"decision":"block","reason":…}` on stdout while exiting 0. On Claude Code the opposite holds: exit
code **2** from a `Stop` hook is itself the block, and the hook's **stderr** is the message. A
Copilot binding dropped into Claude Code exits 0 and never blocks; a Claude binding dropped into
Copilot exits 2 and never blocks. Both failures are silent and both fail **open**.

| harness | event | how it blocks | status |
|---|---|---|---|
| **GitHub Copilot CLI** (§1, §2) | `agentStop` | stdout `{"decision":"block","reason":…}`, exit 0 | **measured**, 1.0.80–1.0.82 |
| **Claude Code** (§2b) | `Stop` | **exit code 2**, message on **stderr** | documented, **not measured** |
| VS Code / IDE agents | — | no documented completion event | **no binding** |

§1, §2 and §5 were measured on Copilot CLI 1.0.80–1.0.82 (Aug–Sep 2026). Re-verify the behaviors in
§5 on the build you are running; the CLI auto-updates, and it changed under two of the measurements
behind this file while they were still running.

## 1. The hooks file — Copilot CLI binding

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

## 2. The `agentStop` script — fail closed (Copilot CLI binding)

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

## 2b. The Claude Code binding — `Stop`, exit 2

**Not measured.** Built from documented behavior: `Stop` is listed as a blocking event whose exit-code-2
effect is *"Prevents Claude from stopping, continues the conversation"*, and the documented rule for
the message is *"the blocking message is the reason from your JSON's blocking decision when it makes
one, and your stderr text otherwise."* This binding takes the stderr path, which the documentation
states plainly, rather than a JSON `decision` shape for `Stop` that it does not. Watch it refuse once
before you trust it (Phase 4 step 6).

Config goes in **`~/.claude/settings.json`** — user-level, outside the repository the agent edits.
`Stop` takes **no matcher**, and an `if` key would disable the hook entirely, since `if` is evaluated
only on tool events.

```json
{
  "hooks": {
    "Stop": [
      { "hooks": [
          { "type": "command",
            "command": "/abs/path/gate/hooks/claude-stop.sh",
            "timeout": 300 }
      ] }
    ]
  }
}
```

```bash
#!/usr/bin/env bash
# claude-stop.sh — Claude Code Stop binding.
# FAIL CLOSED, INVERTED FROM COPILOT: here exit 2 blocks and stderr carries the message.
# exit 0 lets the turn end, so every path that cannot verify must exit 2.
set -uo pipefail
export PATH="/usr/local/bin:/opt/homebrew/bin:$PATH"   # a hook inherits no login shell
IN="$(cat)"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GATE="$HERE/../gate.sh"
GATE_WORK="${GATE_WORK:-$HOME/.corestory-gate}"        # export absolutely; see the sandboxed-HOME trap

block() { printf '%s\n' "$1" >&2; exit 2; }            # <-- the ONLY difference that matters
field() { printf '%s' "$IN" | python3 -c "import json,sys; print(json.load(sys.stdin).get('$1','') or '')" 2>/dev/null; }

TREE="${CLAUDE_PROJECT_DIR:-}"; [ -n "$TREE" ] || TREE="$(field cwd)"; [ -n "$TREE" ] || TREE="$PWD"
[ -d "$TREE" ] || block "GATE COULD NOT EXECUTE — no working tree to judge. Nothing was verified. Blocking rather than passing an unverified change."
[ -r "$GATE" ] || block "GATE COULD NOT EXECUTE — gate script missing at $GATE. Nothing was verified. Blocking."

OUT="$(bash "$GATE" --tree "$TREE" 2>/dev/null)"; RC=$?
[ "$RC" = 0 ] && exit 0                       # the ONLY path that lets the turn end
[ -n "$OUT" ] || OUT="GATE COULD NOT EXECUTE — the gate exited $RC without a message. Nothing was verified. Blocking."

# Claude Code documents no block ceiling the way Copilot documents eight. Cap it here anyway: a Stop
# hook that blocks forever is an agent that cannot hand the ticket back. Count per session.
SID="$(field session_id)"; [ -n "$SID" ] || SID="nosession"
CNT_FILE="$GATE_WORK/blocks.$SID"; mkdir -p "$(dirname "$CNT_FILE")"
N=$(( $(cat "$CNT_FILE" 2>/dev/null || echo 0) + 1 )); echo "$N" > "$CNT_FILE"
if [ "$N" -ge 8 ]; then
  OUT="$OUT

This is the last refusal this gate will raise this session. Fix the behaviour now or hand the ticket back."
  printf '%s\n' "$OUT" >&2; exit 2
fi
block "$OUT"
```

Differences from the Copilot script worth reading twice, because each one fails open if missed:

- **`block()` exits 2 and writes to stderr.** The Copilot version exits **0** and writes JSON to
  stdout. Swapping them yields a hook that runs, reports nothing, and blocks nothing.
- **Exit 0 means "let the turn end."** On exit 0, a hook's stderr goes to the debug log only and the
  model never sees it — so a diagnostic printed on the success path is invisible, not helpful.
- **`CLAUDE_PROJECT_DIR`**, not `COPILOT_PROJECT_DIR`.
- **`session_id`**, not `sessionId`.
- **`timeout` is seconds and sits on the hook object**, not `timeoutSec`.
- Claude Code may expose a field for detecting that a Stop hook is already in the loop it caused.
  This script does not rely on one; the session counter is what bounds it. If you confirm such a
  field on your build, honour it as well — do not replace the counter with it.

**Flag mode** on Claude Code is a `PostToolUse` hook that exits 2, since exit 2 is the documented way
to put a warning in front of the model after a tool has already run. As on Copilot, flag mode must
never exit non-zero for a reason other than the advisory itself.

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
   agent's directory**, and build there. **Exclude every instruction file and every run artifact from
   what is judged** — not just the ones an agent writes. The list is:

   ```
   AGENTS.md  CLAUDE.md  .github/instructions/  .github/copilot-instructions.md
   SPEC.md  REQUEST.md  TICKETS.md  CONSTRAINTS.md  PROVENANCE.md  definition.json
   constraint-tickets/            # the whole run tree: tickets/, decompose-prompt.txt, runs/
   ```

   The first line is the agent's own instruction surface; a gate that judges it lets an agent pass by
   editing what it was told. The rest is this skill's own paperwork, and it is the easier mistake:
   the run artifacts sit in the repository by default (Phase 1, *Where these directories live*), so a
   `git diff` against `HEAD` sweeps them into the patch. Two things then go wrong. The build in the
   pristine worktree can fail on files that are not code, which the gate reports as exit 4 — *could
   not run* — for a change that was fine. And `SPEC.md` gets copied into the worktree the gate
   builds, which is the "spec in the working tree" arm that converted **1 of 5**: the gate would be
   recreating the weakest measured condition inside its own check. Never run the agent's tests — they assert
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

**These six rows test the gate. None of them tests the binding.** They invoke `gate.sh` directly, so
they pass identically whether the hook is wired correctly, wired to the wrong harness, or not
installed at all. Add a seventh check, on the harness you will actually arm: with the gate armed and
a known-broken tree, **start a real session, let the agent try to finish, and watch it be refused** —
then confirm the gate's message appears in the agent's context rather than only in a log. This is
the one failure that the rest of this template cannot catch, and it fails open: the gate returns 1,
the binding swallows it, the agent finishes, and nothing anywhere says so. The two ways to produce
it are in §2b's difference list, and both are one-character-class mistakes — stdout for stderr, exit
0 for exit 2.

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
