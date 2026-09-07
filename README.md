# CoreStory Agent Skills

Installable workflows that teach coding agents how to use [CoreStory](https://corestory.ai) for architecture-grounded software work. This repository packages 19 Agent Skills drawn from CoreStory's 18 public playbooks, and includes the CoreStory remote MCP server configuration.

## Before you install: the MCP URL is per-organization

Every CoreStory organization has its own MCP endpoint:

```
https://app.corestory.ai/mcp/{your-org-slug}-{org-id}
```

The URL identifies the organization, not you. Everyone in an org uses the same URL, and it never spans multiple orgs. Because of that, **this repository cannot ship a working URL** — you supply your own, copied from **CoreStory → Settings → IDE Integrations**. How you supply it differs by tool, so follow the matching section below.

Authentication is browser-based OAuth against CoreStory's identity provider. There is no token to copy or store, and access is limited to the permissions of the signed-in CoreStory user.

## Install

### Claude Code — skills and MCP together

```bash
claude plugin marketplace add corestoryai/agent-skills
claude plugin install corestory@corestory
```

The plugin declares `mcp_url` as required user configuration, so Claude Code prompts you for your organization's URL during install and stores it. If you skip the prompt, the CoreStory server reports that its URL is unset; run `/plugin manage`, select **corestory**, and configure it. Use `/mcp` to complete or refresh the OAuth connection.

### Codex — skills and MCP as two steps

```bash
codex plugin marketplace add corestoryai/agent-skills
codex plugin add corestory@corestory
```

Codex does not expand configuration values inside MCP server declarations, so the Codex plugin manifest declares no MCP server at all, and the URL in each skill's `agents/openai.yaml` is a deliberately unusable placeholder (`https://REPLACE-WITH-YOUR-ORG-MCP-URL.invalid`). **Adding the server is a required manual step:**

```bash
codex mcp add corestory --url https://app.corestory.ai/mcp/your-org-slug-123456789
```

The first CoreStory tool call starts browser-based OAuth. Sign in with the CoreStory account that owns or can access the relevant project.

### Other agents — skills only

The GitHub CLI installs the skills without any MCP configuration:

```bash
gh skill install corestoryai/agent-skills --all --agent codex --scope user
```

Run `gh skill install --help` for the agent targets your `gh` build supports, and pass the one you need to `--agent`. An alternative installer:

```bash
npx skills add corestoryai/agent-skills --skill '*' --agent codex --global --yes --full-depth
```

Neither path configures the MCP connection. Add it yourself with your agent's own MCP configuration mechanism and your organization's URL — for Codex, the `codex mcp add` command above.

Skill layouts, manifests, and MCP capabilities differ across agents. A skills-only install gives an agent the workflows; without a CoreStory MCP connection those workflows will stop at their first grounding step and ask you to configure it.

## Included skills

### Everyday delivery

- `corestory` — project discovery, CoreStory orientation, and workflow routing
- `bug-resolver` — source-grounded root-cause analysis and test-driven bug resolution
- `implement-feature` — architecture-grounded feature delivery with TDD
- `feature-gap-analysis` — pre-implementation gap and dependency analysis
- `using-corestory-with-jira` — Jira intake, enrichment, triage, and requested updates

### Specifications and tests

- `spec-driven-development` — six-phase specification-first delivery, including GitHub Spec Kit integration
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

The plugin declares one remote MCP server, `corestory`, whose URL you provide at install time as described above. It contains no hooks and runs no local executable code. The MCP connection uses browser-based OAuth and is limited by the signed-in user's CoreStory permissions.

Reading and analysis are the default in every skill. Some skills can edit the repository, or an explicitly connected system such as Jira, when you ask the agent to do so — see [`SOURCES.md`](SOURCES.md) for the itemized list of behaviors that require an explicit request.

Review [`plugins/corestory/.mcp.json`](plugins/corestory/.mcp.json) and the individual `SKILL.md` files before installing if you want to inspect the exact behavior.

## Validate a checkout

```bash
python3 scripts/validate-release.py
python3 scripts/build-catalog.py --check
gh skill publish --dry-run
claude plugin validate plugins/corestory
claude plugin validate .
```

## Discovery and republishing

The repository includes an Agent Skills discovery catalog at [`.well-known/agent-skills/index.json`](.well-known/agent-skills/index.json), carrying a sha256 digest per skill. Every edit to a `SKILL.md` invalidates its digest, so re-run the catalog build after any content change:

```bash
python3 scripts/build-catalog.py
```

To generate a docs-host-ready tree with lowercase `skill.md` paths:

```bash
python3 scripts/export-well-known.py --output-dir dist/well-known
```

See [`SOURCES.md`](SOURCES.md) for the public CoreStory source behind every packaged skill.

## Status and support

This is CoreStory's canonical public skills repository. The Agent Skills ecosystem and vendor plugin directories are evolving; releases are versioned so installations can be pinned and audited.

- Product and account setup: [CoreStory documentation](https://docs.corestory.ai)
- Security reports: see [`SECURITY.md`](SECURITY.md)

No open-source license is included in this release.
