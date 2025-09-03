#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ADR_DIR = ROOT / "docs" / "adr"

TITLE_RE = re.compile(r"^#\s+\d+\.\s+.+$")
DATE_RE = re.compile(r"^Date:\s+\d{4}-\d{2}-\d{2}$")
STATUS_RE = re.compile(r"^##\s+Status$", re.IGNORECASE)


def check_adr(path: Path) -> list[str]:
    problems: list[str] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception as e:
        return [f"cannot read: {e}"]

    # Title
    if not lines or not TITLE_RE.match(lines[0].strip()):
        problems.append("missing or malformed title '# <N>. <Title>' on line 1")

    # Date
    if not any(DATE_RE.match(ln.strip()) for ln in lines[:20]):
        problems.append("missing 'Date: YYYY-MM-DD' in top section")

    # Status section exists
    if not any(STATUS_RE.match(ln.strip()) for ln in lines):
        problems.append("missing '## Status' section")

    return problems


def main() -> int:
    if not ADR_DIR.exists():
        print(f"ADR directory not found: {ADR_DIR}", file=sys.stderr)
        return 1
    bad = []
    for path in sorted(ADR_DIR.glob("*.md")):
        probs = check_adr(path)
        if probs:
            bad.append((path, probs))
    if bad:
        print("ADR validation failed:")
        for p, probs in bad:
            print(f"- {p.relative_to(ROOT)}:")
            for pr in probs:
                print(f"  * {pr}")
        return 1
    print("ADR validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

