#!/usr/bin/env python3
"""Export a docs-host-ready .well-known Agent Skills tree."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins" / "corestory" / "skills"


def metadata(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise ValueError(f"{path}: missing YAML frontmatter")
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, separator, raw = line.partition(":")
        if separator and key in {"name", "description"}:
            raw = raw.strip()
            values[key] = json.loads(raw) if raw.startswith('"') else raw
    return values["name"], values["description"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--public-base-url",
        default="https://docs.corestory.ai/.well-known/agent-skills",
    )
    args = parser.parse_args()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    entries = []
    for source in sorted(SKILLS.glob("*/SKILL.md")):
        name, description = metadata(source)
        target = output / name / "skill.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        entries.append(
            {
                "name": name,
                "type": "skill-md",
                "description": description,
                "url": f"{args.public_base_url.rstrip('/')}/{name}/skill.md",
                "digest": f"sha256:{hashlib.sha256(source.read_bytes()).hexdigest()}",
            }
        )
    payload = {
        "$schema": "https://schemas.agentskills.io/discovery/0.2.0/schema.json",
        "skills": entries,
    }
    (output / "index.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Exported {len(entries)} skills to {output}")


if __name__ == "__main__":
    main()
