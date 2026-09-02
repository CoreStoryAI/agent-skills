# CoreStory Agent Skills

Installable workflows that teach coding agents how to use [CoreStory](https://corestory.ai) for architecture-grounded software work. This repository packages 20 public CoreStory playbooks as portable Agent Skills and includes the CoreStory remote MCP server configuration.

## Recommended installs

### Codex — skills and MCP together

```bash
codex plugin marketplace add corestoryai/agent-skills
codex plugin add corestory@corestory
```

The first CoreStory tool call starts browser-based OAuth. Sign in with the CoreStory account that owns or can access the relevant project.

### Claude Code — skills and MCP together

```bash
claude plugin marketplace add corestoryai/agent-skills
claude plugin install corestory@corestory
```

Use `/mcp` in Claude Code if you need to complete or refresh the CoreStory OAuth connection.

### Any supported coding agent — skills only

The GitHub CLI can install all skills for Codex, Claude Code, GitHub Copilot, Cursor, Gemini CLI, and many other agents:

```bash
gh skill install corestoryai/agent-skills --all --agent codex --scope user
```

Change `--agent codex` to the target shown by `gh skill install --help`. A skills-only install does not install the MCP connection; configure the remote server separately:

```bash
codex mcp add corestory --url https://app.corestory.ai/mcp
```

The installer referenced by the original CoreStory UX report also discovers all 20 skills:

```bash
npx skills add corestoryai/agent-skills --skill '*' --agent codex --global --yes --full-depth
```

The universal endpoint uses OAuth. If CoreStory cannot select the correct organization after sign-in, replace it with the organization-specific URL from **CoreStory → Settings → IDE Integrations**.

## Included skills

### Everyday delivery

- `corestory` — project discovery, CoreStory orientation, and workflow routing
- `bug-resolver` — source-grounded root-cause analysis and test-driven bug resolution
- `implement-feature` — architecture-grounded feature delivery with TDD
- `feature-gap-analysis` — pre-implementation gap and dependency analysis
- `using-corestory-with-jira` — Jira intake, enrichment, triage, and requested updates

### Specifications and tests

- `spec-driven-development` — six-phase specification-first delivery
- `spec-kit-companion` — CoreStory grounding for GitHub Spec Kit artifacts
- `spec-driven-test-generation` — router for behavioral and E2E testing
- `generate-tests` — unit- and integration-level behavioral coverage
- `generate-e2e-tests` — critical user-journey coverage

### Modernization

- `code-modernization` — governed six-phase modernization router
- `codebase-assessment` — modernization readiness assessment
- `business-rules-extraction` — source-verified business-rule inventory
- `target-architecture` — strategy selection and target-state ADR
- `decomposition-sequencing` — dependency-aware work packages
- `monolith-to-microservices` — Strangler Fig service extraction
- `behavioral-verification` — legacy-to-target equivalence verification
- `vibe-modernization` — source-grounded legacy-to-target migration arc
- `vibe-conformance-audit` — independent anti-circular completeness audit

### Technical diligence

- `ma-technical-due-diligence` — architecture, quality, risk, and integration assessment

## What this package can access

The plugin declares one remote MCP server: `https://app.corestory.ai/mcp`. It contains no hooks and runs no local executable code. The MCP connection uses browser-based OAuth and is limited by the signed-in user's CoreStory permissions. Some skills can edit the repository or an explicitly connected system such as Jira when the user asks the agent to do so.

Review [`plugins/corestory/.mcp.json`](plugins/corestory/.mcp.json) and the individual `SKILL.md` files before installing if you want to inspect the exact behavior.

## Validate a checkout

```bash
python3 scripts/validate-release.py
gh skill publish --dry-run
claude plugin validate plugins/corestory
claude plugin validate .
```

## Discovery and republishing

The repository includes an Agent Skills discovery catalog at [`.well-known/agent-skills/index.json`](.well-known/agent-skills/index.json). To generate a docs-host-ready tree with lowercase `skill.md` paths:

```bash
python3 scripts/export-well-known.py --output-dir dist/well-known
```

See [`SOURCES.md`](SOURCES.md) for the public CoreStory playbook behind every packaged skill.

## Status and support

This is CoreStory's canonical public skills repository. The Agent Skills ecosystem and vendor plugin directories are evolving; releases are versioned so installations can be pinned and audited.

- Product and account setup: [CoreStory documentation](https://docs.corestory.ai)
- Security reports: see [`SECURITY.md`](SECURITY.md)

No open-source license is included in this release.
