#!/usr/bin/env python3
"""Validate Agent Workbench skill metadata, provenance, and role cards."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_skill_file(path: Path) -> Tuple[Dict[str, str], str]:
    """Parse the deliberately small single-line YAML frontmatter subset used here."""
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        raise ValueError("frontmatter must start with '---'")
    closing = content.find("\n---\n", 4)
    if closing < 0:
        raise ValueError("frontmatter closing '---' not found")
    fields: Dict[str, str] = {}
    for line_number, line in enumerate(content[4:closing].splitlines(), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line {line_number}: expected key: value")
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if not key or not value:
            raise ValueError(f"invalid frontmatter line {line_number}: key and value are required")
        if key in fields:
            raise ValueError(f"duplicate frontmatter key: {key}")
        fields[key] = value
    return fields, content[closing + len("\n---\n"):].strip()


def validate_skill_file(path: Path, expected_name: str | None = None) -> List[str]:
    errors: List[str] = []
    try:
        fields, body = parse_skill_file(path)
    except (OSError, UnicodeError, ValueError) as exc:
        return [f"{path}: {exc}"]
    for required in ("name", "description"):
        if required not in fields:
            errors.append(f"{path}: missing required '{required}' field")
    name = fields.get("name", "")
    description = fields.get("description", "")
    if name and not NAME_PATTERN.fullmatch(name):
        errors.append(f"{path}: name must be a lowercase hyphenated slug")
    if name and len(name) > 64:
        errors.append(f"{path}: name exceeds 64 characters")
    if expected_name and name and name != expected_name:
        errors.append(f"{path}: name '{name}' does not match folder '{expected_name}'")
    if description and len(description) > 1024:
        errors.append(f"{path}: description exceeds 1024 characters")
    if len(body) < 160:
        errors.append(f"{path}: instructions are too short to define an operational workflow")
    return errors


def validate_skills_directory(skills_dir: Path) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    if not skills_dir.is_dir():
        return [f"missing skills directory: {skills_dir}"], []
    skill_dirs = sorted(path for path in skills_dir.iterdir() if path.is_dir())
    if not skill_dirs:
        return [f"no skill directories found in {skills_dir}"], []
    names: List[str] = []
    for skill_dir in skill_dirs:
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"{skill_dir}: missing SKILL.md")
            continue
        errors.extend(validate_skill_file(skill_file, expected_name=skill_dir.name))
        names.append(skill_dir.name)
    if len(names) != len(set(names)):
        errors.append("duplicate skill directory names found")
    return errors, names


def validate_sources(path: Path, skill_names: List[str]) -> List[str]:
    errors: List[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"{path}: cannot read valid JSON: {exc}"]
    if not isinstance(data, dict):
        return [f"{path}: top-level JSON value must be an object"]
    upstream = data.get("upstream_sources")
    mapping = data.get("skill_sources")
    if not isinstance(upstream, dict) or not isinstance(mapping, dict):
        return [f"{path}: expected upstream_sources and skill_sources objects"]
    for source_id, source in upstream.items():
        if not isinstance(source, dict):
            errors.append(f"{path}: source '{source_id}' must be an object")
            continue
        url = source.get("url")
        if not isinstance(url, str) or not url.startswith("https://"):
            errors.append(f"{path}: source '{source_id}' must have an HTTPS URL")
        for required in ("license", "role"):
            value = source.get(required)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{path}: source '{source_id}' is missing '{required}'")
    missing = sorted(set(skill_names) - set(mapping))
    extra = sorted(set(mapping) - set(skill_names))
    if missing:
        errors.append(f"{path}: skills missing source mapping: {', '.join(missing)}")
    if extra:
        errors.append(f"{path}: source mapping references unknown skills: {', '.join(extra)}")
    for skill, entry in mapping.items():
        if not isinstance(entry, dict) or entry.get("relationship") not in {
            "original", "workflow-inspired; instruction text independently written"
        }:
            errors.append(f"{path}: invalid relationship for {skill}")
            continue
        refs = entry.get("sources")
        if not isinstance(refs, list):
            errors.append(f"{path}: sources for {skill} must be a list")
            continue
        if entry["relationship"] == "original" and refs:
            errors.append(f"{path}: original skill {skill} must not list upstream sources")
        if entry["relationship"] != "original" and not refs:
            errors.append(f"{path}: inspired skill {skill} must list at least one source")
        for ref in refs:
            if not isinstance(ref, str):
                errors.append(f"{path}: source references for {skill} must be strings")
            elif ref not in upstream:
                errors.append(f"{path}: {skill} references unknown source '{ref}'")
    return errors


def validate_role_cards(agents_dir: Path) -> Tuple[List[str], int]:
    errors: List[str] = []
    if not agents_dir.is_dir():
        return [f"missing agents directory: {agents_dir}"], 0
    cards = sorted(path for path in agents_dir.glob("*.md") if path.name.lower() != "readme.md")
    if not cards:
        return [f"no agent role cards found in {agents_dir}"], 0
    required_sections = ("## Mission", "## Responsibilities", "## Output contract", "## Boundaries")
    for card in cards:
        try:
            content = card.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{card}: {exc}")
            continue
        for section in required_sections:
            if section not in content:
                errors.append(f"{card}: missing section {section}")
        if len(content) < 180:
            errors.append(f"{card}: role card is too short")
    return errors, len(cards)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    root = parser.parse_args().root
    errors, names = validate_skills_directory(root / "skills")
    errors.extend(validate_sources(root / "sources.json", names))
    role_errors, role_count = validate_role_cards(root / "agents")
    errors.extend(role_errors)
    if errors:
        for error in errors:
            print(f"[FAIL] {error}", file=sys.stderr)
        print(f"Validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1
    print(f"[OK] {len(names)} skill manifests and source mappings validated.")
    print(f"[OK] {role_count} portable agent role cards validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
