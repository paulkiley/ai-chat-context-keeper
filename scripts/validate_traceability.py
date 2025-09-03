#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ADR_DIR = ROOT / "docs" / "adr"
TRACE = ROOT / "docs" / "traceability.json"

TITLE_RE = re.compile(r"^#\s+(\d+)\.\s+.+$")


def collect_adr_ids() -> set[str]:
    ids: set[str] = set()
    for p in ADR_DIR.glob("*.md"):
        try:
            first = p.read_text(encoding="utf-8").splitlines()[0].strip()
        except Exception:
            continue
        m = TITLE_RE.match(first)
        if m:
            ids.add(m.group(1))
    return ids


def validate_traceability() -> list[str]:
    problems: list[str] = []
    if not TRACE.exists():
        return [f"missing {TRACE.relative_to(ROOT)}"]
    try:
        data = json.loads(TRACE.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"invalid JSON: {e}"]

    adrs_present = collect_adr_ids()
    inits = data.get("initiatives", [])
    if not isinstance(inits, list):
        problems.append("initiatives must be a list")
        return problems

    for i, init in enumerate(inits, 1):
        if not isinstance(init, dict):
            problems.append(f"initiative[{i}] is not an object")
            continue
        adr_list = init.get("adrs", [])
        for adr in adr_list:
            if adr not in adrs_present:
                problems.append(f"initiative {init.get('id','?')}: ADR {adr} not found in docs/adr/")
    return problems


def main() -> int:
    probs = validate_traceability()
    if probs:
        print("Traceability validation failed:")
        for p in probs:
            print(f"- {p}")
        return 1
    print("Traceability validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

