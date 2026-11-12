#!/usr/bin/env python3
"""Dependency-free release validation for the CoreStory skills repository."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGINS = {
    "corestory": ROOT / "plugins" / "corestory",
    "corestory-local": ROOT / "plugins" / "corestory-local",
}
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
EXPECTED_VERSION = "1.0.0"
MCP_URL_EXPANSION = "${user_config.mcp_url}"
CODEX_PLACEHOLDER = "https://REPLACE-WITH-YOUR-ORG-MCP-URL.invalid"
BARE_MCP_URL_RE = re.compile(r"app\.corestory\.ai/mcp(?![/\w-])")


def frontmatter(path: Path) -> dict[str, str]:
    """Parse the supported single-line YAML frontmatter fields."""
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
    """Load a JSON object from path."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected JSON object")
    return payload


def validate_skills(plugin: str, skills: Path, errors: list[str]) -> set[str]:
    """Validate every skill and agent descriptor in one plugin."""
    skill_files = sorted(skills.glob("*/SKILL.md"))
    expected_count = 20 if plugin == "corestory" else 6
    if len(skill_files) != expected_count:
        errors.append(f"{plugin}: expected {expected_count} skills, found {len(skill_files)}")
    names: set[str] = set()
    for path in skill_files:
        try:
            fields = frontmatter(path)
            name = fields.get("name", "")
            description = fields.get("description", "")
            if set(fields) != {"name", "description", "license"}:
                errors.append(f"{path}: frontmatter must contain name, description, and license")
            if fields.get("license") != "MIT":
                errors.append(f"{path}: license must be MIT")
            if name != path.parent.name:
                errors.append(f"{path}: name does not match directory")
            if not NAME_RE.fullmatch(name) or len(name) > 64:
                errors.append(f"{path}: invalid Agent Skills name")
            if not description or len(description) > 1024 or "<" in description or ">" in description:
                errors.append(f"{path}: invalid description")
            if name in names:
                errors.append(f"{path}: duplicate skill name in {plugin}")
            names.add(name)
            if "[TODO:" in path.read_text(encoding="utf-8"):
                errors.append(f"{path}: unfinished placeholder")
            openai = path.parent / "agents" / "openai.yaml"
            if not openai.exists() or f"${name}" not in openai.read_text(encoding="utf-8"):
                errors.append(f"{path.parent}: missing or invalid agents/openai.yaml")
        except (KeyError, ValueError, json.JSONDecodeError) as error:
            errors.append(str(error))
    return names


def main() -> None:
    """Validate published skills, manifests, and the discovery catalog."""
    errors: list[str] = []
    skill_names = {
        plugin: validate_skills(plugin, plugin_root / "skills", errors)
        for plugin, plugin_root in PLUGINS.items()
    }
    manifests = {
        plugin: (
            validate_json(plugin_root / ".codex-plugin" / "plugin.json"),
            validate_json(plugin_root / ".claude-plugin" / "plugin.json"),
            validate_json(plugin_root / ".mcp.json"),
        )
        for plugin, plugin_root in PLUGINS.items()
    }
    codex_market = validate_json(ROOT / ".agents" / "plugins" / "marketplace.json")
    claude_market = validate_json(ROOT / ".claude-plugin" / "marketplace.json")
    catalog = validate_json(ROOT / ".well-known" / "agent-skills" / "index.json")
    gemini = validate_json(ROOT / "gemini-extension.json")

    for plugin, (codex, claude, mcp) in manifests.items():
        for manifest, label in ((codex, "Codex"), (claude, "Claude")):
            if manifest.get("name") != plugin or manifest.get("version") != EXPECTED_VERSION:
                errors.append(f"{plugin}: {label} plugin manifest identity/version mismatch")
        servers = mcp.get("mcpServers", {})
        server = servers.get(plugin, {}) if isinstance(servers, dict) else {}
        if not isinstance(server, dict):
            errors.append(f"{plugin}: MCP server configuration is invalid")
            continue
        if plugin == "corestory":
            if server.get("url") != MCP_URL_EXPANSION:
                errors.append(f"{plugin}: MCP endpoint must be {MCP_URL_EXPANSION!r}")
            user_config = claude.get("userConfig")
            field = user_config.get("mcp_url") if isinstance(user_config, dict) else None
            if not isinstance(field, dict) or field.get("type") != "string" or field.get("required") is not True:
                errors.append("corestory: Claude manifest must require userConfig.mcp_url")
            for path in sorted((PLUGINS[plugin] / "skills").glob("*/agents/openai.yaml")):
                text = path.read_text(encoding="utf-8")
                if BARE_MCP_URL_RE.search(text):
                    errors.append(f"{path}: bare MCP URL")
                if CODEX_PLACEHOLDER not in text or "codex mcp add corestory --url" not in text:
                    errors.append(f"{path}: missing required CoreStory MCP guidance")
        else:
            if server.get("command") != "corestory" or server.get("args") != ["mcp", "--path", "${workspaceFolder}", "--no-watch"]:
                errors.append("corestory-local: MCP server must start the local binary with workspace scope and no watch")

    for marketplace, label in ((codex_market, "Codex"), (claude_market, "Claude")):
        plugins = marketplace.get("plugins")
        names = {entry.get("name") for entry in plugins if isinstance(entry, dict)} if isinstance(plugins, list) else set()
        if names != set(PLUGINS):
            errors.append(f"{label} marketplace must list exactly {', '.join(PLUGINS)}")

    gemini_servers = gemini.get("mcpServers")
    gemini_local = gemini_servers.get("corestory-local") if isinstance(gemini_servers, dict) else None
    if (gemini.get("name") != "corestory-local"
            or gemini.get("version") != EXPECTED_VERSION
            or not isinstance(gemini_local, dict)
            or gemini_local.get("command") != "corestory"
            or gemini_local.get("args") != ["mcp", "--path", "${workspacePath}", "--no-watch"]):
        errors.append("Gemini extension must expose the workspace-scoped corestory-local MCP server")

    entries = catalog.get("skills", [])
    actual_catalog = {
        (entry.get("plugin"), entry.get("name"))
        for entry in entries
        if isinstance(entry, dict)
    } if isinstance(entries, list) else set()
    expected_catalog = {(plugin, name) for plugin, names in skill_names.items() for name in names}
    if actual_catalog != expected_catalog:
        errors.append("discovery catalog does not match packaged skills")

    if errors:
        print("Release validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    total = sum(len(names) for names in skill_names.values())
    print(f"Release validation passed: {total} skills across {len(PLUGINS)} plugins")


if __name__ == "__main__":
    main()
