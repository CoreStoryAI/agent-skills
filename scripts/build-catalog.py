#!/usr/bin/env python3
"""Build the repository's Agent Skills discovery catalog."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins" / "corestory" / "skills"
DEFAULT_OUTPUT = ROOT / ".well-known" / "agent-skills" / "index.json"
DEFAULT_BASE_URL = "https://raw.githubusercontent.com/corestoryai/agent-skills/main/plugins/corestory/skills"


def parse_frontmatter(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise ValueError(f"{path}: missing YAML frontmatter")
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, separator, raw = line.partition(":")
        if separator and key in {"name", "description"}:
            raw = raw.strip()
            fields[key] = json.loads(raw) if raw.startswith('"') else raw
    return fields["name"], fields["description"]


def catalog(base_url: str, filename: str) -> dict[str, object]:
    entries = []
    for skill_file in sorted(SKILLS.glob("*/SKILL.md")):
        name, description = parse_frontmatter(skill_file)
        digest = hashlib.sha256(skill_file.read_bytes()).hexdigest()
        entries.append(
            {
                "name": name,
                "type": "skill-md",
                "description": description,
                "url": f"{base_url.rstrip('/')}/{name}/{filename}",
                "digest": f"sha256:{digest}",
            }
        )
    return {
        "$schema": "https://schemas.agentskills.io/discovery/0.2.0/schema.json",
        "skills": entries,
    }


def render(payload: dict[str, object]) -> str:
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--filename", default="SKILL.md")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = render(catalog(args.base_url, args.filename))
    output = args.output.resolve()
    if args.check:
        actual = output.read_text(encoding="utf-8") if output.exists() else ""
        if actual != expected:
            raise SystemExit(f"Catalog is stale: {output}")
        print(f"Catalog is current: {output}")
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(expected, encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
