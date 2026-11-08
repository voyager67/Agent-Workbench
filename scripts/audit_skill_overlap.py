#!/usr/bin/env python3
"""Report possible skill-routing overlap using lexical Jaccard similarity."""
from __future__ import annotations

import argparse
import itertools
import re
from pathlib import Path

STOP = {"about", "after", "also", "and", "any", "are", "before", "by", "can", "for", "from", "into", "its", "not", "of", "on", "or", "the", "to", "use", "when", "with", "work", "your", "this", "that", "where", "which", "while"}


def tokens(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8").lower()
    # Compare activation descriptions and headings; ignore body details to keep routing focus.
    lines = text.splitlines()
    selected = []
    in_frontmatter = False
    for line in lines:
        if line.strip() == "---":
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter or line.startswith("#"):
            selected.append(line)
    words = re.findall(r"[a-z][a-z0-9-]{2,}", " ".join(selected))
    return {word for word in words if word not in STOP}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--threshold", type=float, default=0.28)
    args = parser.parse_args()
    if not 0 < args.threshold <= 1:
        parser.error("--threshold must be between 0 and 1")
    files = sorted((args.root / "skills").glob("*/SKILL.md"))
    sets = {p.parent.name: tokens(p) for p in files}
    hits = []
    for (name_a, set_a), (name_b, set_b) in itertools.combinations(sets.items(), 2):
        union = set_a | set_b
        score = len(set_a & set_b) / len(union) if union else 0.0
        if score >= args.threshold:
            hits.append((score, name_a, name_b, sorted(set_a & set_b)))
    if not hits:
        print(f"[OK] No lexical overlap pairs at threshold {args.threshold:.2f} across {len(files)} skills.")
        return 0
    print(f"Potential routing overlap (lexical heuristic; threshold={args.threshold:.2f}):")
    for score, a, b, common in sorted(hits, reverse=True):
        print(f"  {score:.2f}  {a} <-> {b}  shared: {', '.join(common[:12])}")
    print("Review these pairs manually. Similar words do not prove duplicate behavior.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
