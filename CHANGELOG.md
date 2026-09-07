# Changelog

## 1.0.0 — unreleased

- Publish 19 Agent Skills drawn from CoreStory's 18 public playbooks: 16 lifted from playbook skill
  blocks, 2 hand-authored, 1 copied from the published skill reference.
- Fold the Spec Kit companion content into `spec-driven-development` as a `.specify/`-gated section,
  matching the playbook, which presents it as an append rather than a standalone skill.
- Add combined Codex and Claude Code plugin packages.
- Add the OAuth-enabled CoreStory remote MCP configuration. The MCP URL is per-organization, so
  Claude Code prompts for it at install via `userConfig.mcp_url`; Codex requires a manual
  `codex mcp add corestory --url <your org URL>`.
- Add GitHub CLI, `npx skills`, Codex marketplace, and Claude marketplace install paths.
- Add a digest-backed Agent Skills discovery catalog and docs-host export utility.
- Add local and CI release validation.
- License the release under MIT and set every skill's `license` frontmatter to `MIT`.
- Disclose in `SOURCES.md` every playbook side effect that this package converted from a default to
  an explicit request, and every correction applied to the source material.
