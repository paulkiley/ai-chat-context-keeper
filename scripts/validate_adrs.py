#!/usr/bin/env python3
from __future__ import annotations

import os
import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ADR_DIR = ROOT / "docs" / "adr"

TITLE_RE = re.compile(r"^#\s+\d+\.\s+.+$")
DATE_RE = re.compile(r"^Date:\s+\d{4}-\d{2}-\d{2}$")
STATUS_RE = re.compile(r"^##\s+Status$", re.IGNORECASE)
META_RE = re.compile(r"^##\s+Metadata$", re.IGNORECASE)
SEC_RE = re.compile(r"^##\s+Security\s*&\s*Privacy", re.IGNORECASE)

def parse_date(lines: list[str]) -> str | None:
    for ln in lines[:20]:
        s = ln.strip()
        if DATE_RE.match(s):
            return s.split(":", 1)[1].strip()
    return None


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

    # Enforcement threshold for new ADRs
    enforce_date = os.environ.get("ADR_ENFORCE_DATE", "2025-09-03")
    adr_date = parse_date(lines) or "1900-01-01"

    # Metadata section exists
    meta_ok = any(META_RE.match(ln.strip()) for ln in lines)
    if not meta_ok:
        if adr_date >= enforce_date:
            problems.append("missing '## Metadata' section (required for new ADRs)")
        else:
            print(f"WARN {path.name}: missing '## Metadata' (legacy)")

    # Security & Privacy section exists
    sec_ok = any(SEC_RE.match(ln.strip()) for ln in lines)
    if not sec_ok:
        if adr_date >= enforce_date:
            problems.append("missing '## Security & Privacy Considerations' (required for new ADRs)")
        else:
            print(f"WARN {path.name}: missing '## Security & Privacy' (legacy)")

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
