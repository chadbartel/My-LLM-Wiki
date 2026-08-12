#!/usr/bin/env python3
"""Simple linting for the My-LLM-Wiki knowledge base.

Checks for common maintenance issues before synthesis or large queries.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "Wiki"


def find_markdown_files(base: Path):
    return sorted(base.rglob("*.md"))


def check_links(files):
    problems = []
    wikilink_pattern = re.compile(r"\[\[([^\]]+)\]\]")

    for file in files:
        text = file.read_text(encoding="utf-8", errors="ignore")
        for match in wikilink_pattern.findall(text):
            target = match.strip()
            if not target:
                continue
            if "/" in target:
                target = target.split("/")[-1]
            path = (file.parent / target).resolve()
            if not path.exists() and not (WIKI / target).exists():
                problems.append(f"Broken wikilink in {file.relative_to(ROOT)}: {target}")
    return problems


def main():
    files = find_markdown_files(WIKI)
    problems = check_links(files)
    if problems:
        print("Wiki lint issues found:")
        for problem in problems:
            print(f"- {problem}")
        raise SystemExit(1)

    print(f"Wiki lint passed for {len(files)} markdown files.")


if __name__ == "__main__":
    main()
