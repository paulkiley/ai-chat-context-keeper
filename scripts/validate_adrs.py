#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADR_DIR = ROOT / "docs" / "adr"

TITLE_RE = re.compile(r"^#\s+\d+\.\s+.+$")
DATE_RE = re.compile(r"^Date:\s+\d{4}-\d{2}-\d{2}$")
STATUS_RE = re.compile(r"^##\s+Status$", re.IGNORECASE)
META_RE = re.compile(r"^##\s+Metadata$", re.IGNORECASE)
SEC_RE = re.compile(r"^##\s+Security\s*&\s*Privacy", re.IGNORECASE)


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

    # Metadata section exists (warn only for legacy ADRs)
    if not any(META_RE.match(ln.strip()) for ln in lines):
        problems.append(("warn", "missing '## Metadata' section (warn only for legacy ADRs)"))

    # Security & Privacy section exists (warn only for legacy ADRs)
    if not any(SEC_RE.match(ln.strip()) for ln in lines):
        problems.append(("warn", "missing '## Security & Privacy Considerations' section (warn only for legacy ADRs)"))

    return problems


def main() -> int:
    if not ADR_DIR.exists():
        print(f"ADR directory not found: {ADR_DIR}", file=sys.stderr)
        return 1
    bad = []
    for path in sorted(ADR_DIR.glob("*.md")):
        if path.name.lower().startswith("0000-template"):
            continue
        probs = check_adr(path)
        if probs:
            bad.append((path, probs))
    if bad:
        fatal = False
        print("ADR validation report:")
        for p, probs in bad:
            print(f"- {p.relative_to(ROOT)}:")
            for pr in probs:
                if isinstance(pr, tuple) and pr[0] == "warn":
                    print(f"  * WARN: {pr[1]}")
                else:
                    print(f"  * {pr}")
                    fatal = True
        if fatal:
            return 1
        else:
            print("Only warnings detected (legacy ADRs)")
            return 0
    print("ADR validation passed.")
    return 0


# AUTOGEN PATCH


if __name__ == "__main__":
    raise SystemExit(main())
