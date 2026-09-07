#!/usr/bin/env python3
"""Dependency-free release validation for the CoreStory skills repository."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "corestory"
SKILLS = PLUGIN / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
EXPECTED_VERSION = "1.0.0"
# Every CoreStory org has its own MCP URL (https://app.corestory.ai/mcp/{org-slug}-{org-id}).
# A public plugin therefore cannot ship a working URL. Claude Code prompts for it at install
# via userConfig and expands it here; Codex has no equivalent, so it gets a placeholder that
# cannot be mistaken for a default (.invalid is reserved by RFC 2606).
MCP_URL_EXPANSION = "${user_config.mcp_url}"
CODEX_PLACEHOLDER = "https://REPLACE-WITH-YOUR-ORG-MCP-URL.invalid"
BARE_MCP_URL_RE = re.compile(r"app\.corestory\.ai/mcp(?![/\w-])")


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n\n(.+)", text, re.DOTALL)
    if not match:
        raise ValueError(f"{path}: missing frontmatter or body")
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, separator, raw = line.partition(":")
        if not separator:
            raise ValueError(f"{path}: unsupported multiline frontmatter")
        raw = raw.strip()
        values[key] = json.loads(raw) if raw.startswith('"') else raw
    return values


def validate_json(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected JSON object")
    return payload


def main() -> None:
    errors: list[str] = []
    skill_files = sorted(SKILLS.glob("*/SKILL.md"))
    if len(skill_files) != 19:
        errors.append(f"expected 19 skills, found {len(skill_files)}")
    names: set[str] = set()
    for path in skill_files:
        try:
            fields = frontmatter(path)
            name = fields.get("name", "")
            description = fields.get("description", "")
            if set(fields) != {"name", "description", "license"}:
                errors.append(f"{path}: frontmatter must contain name, description, and license")
            if fields.get("license") != "Proprietary":
                errors.append(f"{path}: license must be Proprietary")
            if name != path.parent.name:
                errors.append(f"{path}: name does not match directory")
            if not NAME_RE.fullmatch(name) or len(name) > 64:
                errors.append(f"{path}: invalid Agent Skills name")
            if not description or len(description) > 1024 or "<" in description or ">" in description:
                errors.append(f"{path}: invalid description")
            if name in names:
                errors.append(f"{path}: duplicate skill name")
            names.add(name)
            if "[TODO:" in path.read_text(encoding="utf-8"):
                errors.append(f"{path}: unfinished placeholder")
            openai = path.parent / "agents" / "openai.yaml"
            if not openai.exists() or f"${name}" not in openai.read_text(encoding="utf-8"):
                errors.append(f"{path.parent}: missing or invalid agents/openai.yaml")
        except (KeyError, ValueError, json.JSONDecodeError) as error:
            errors.append(str(error))

    codex = validate_json(PLUGIN / ".codex-plugin" / "plugin.json")
    claude = validate_json(PLUGIN / ".claude-plugin" / "plugin.json")
    mcp = validate_json(PLUGIN / ".mcp.json")
    codex_market = validate_json(ROOT / ".agents" / "plugins" / "marketplace.json")
    claude_market = validate_json(ROOT / ".claude-plugin" / "marketplace.json")
    catalog = validate_json(ROOT / ".well-known" / "agent-skills" / "index.json")

    for manifest, label in [(codex, "Codex"), (claude, "Claude")]:
        if manifest.get("name") != "corestory" or manifest.get("version") != EXPECTED_VERSION:
            errors.append(f"{label} plugin manifest identity/version mismatch")
    servers = mcp.get("mcpServers", {})
    corestory_server = servers.get("corestory", {}) if isinstance(servers, dict) else {}
    if not isinstance(corestory_server, dict) or corestory_server.get("url") != MCP_URL_EXPANSION:
        errors.append(
            f"CoreStory MCP endpoint must be {MCP_URL_EXPANSION!r}: the URL is per-organization, "
            "so a public plugin cannot hard-code one"
        )
    user_config = claude.get("userConfig")
    if not isinstance(user_config, dict) or "mcp_url" not in user_config:
        errors.append("Claude plugin manifest must declare userConfig.mcp_url so install prompts for the org URL")
    else:
        field = user_config["mcp_url"]
        if not isinstance(field, dict):
            errors.append("userConfig.mcp_url must be an object")
        else:
            if field.get("type") != "string":
                errors.append("userConfig.mcp_url.type must be string")
            if field.get("required") is not True:
                errors.append("userConfig.mcp_url.required must be true")
            for key in ("title", "description"):
                if not field.get(key):
                    errors.append(f"userConfig.mcp_url.{key} is required")
    for path in sorted(SKILLS.glob("*/agents/openai.yaml")):
        text = path.read_text(encoding="utf-8")
        if BARE_MCP_URL_RE.search(text):
            errors.append(f"{path}: bare MCP URL; Codex cannot expand config, use the invalid placeholder")
        if CODEX_PLACEHOLDER not in text:
            errors.append(f"{path}: missing the {CODEX_PLACEHOLDER} placeholder")
        if "codex mcp add corestory --url" not in text:
            errors.append(f"{path}: must document the manual 'codex mcp add corestory --url' step")
    if codex_market.get("name") != "corestory":
        errors.append("Codex marketplace name mismatch")
    if claude_market.get("name") != "corestory":
        errors.append("Claude marketplace name mismatch")
    entries = catalog.get("skills", [])
    catalog_names = {
        entry.get("name") for entry in entries if isinstance(entry, dict)
    } if isinstance(entries, list) else set()
    if catalog_names != names:
        errors.append("discovery catalog does not match packaged skills")
    for old_name in ("`spec-driven-dev`", "`feature-implementation`", "`e2e-test-generation`", "fix-bug skill"):
        hits = [str(path) for path in skill_files if old_name in path.read_text(encoding="utf-8")]
        if hits:
            errors.append(f"stale cross-skill reference {old_name}: {', '.join(hits)}")

    if errors:
        print("Release validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print(f"Release validation passed: {len(skill_files)} skills, plugin version {EXPECTED_VERSION}")


if __name__ == "__main__":
    main()
