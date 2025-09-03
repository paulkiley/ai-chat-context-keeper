#!/usr/bin/env python3
import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

NEW_REPO = "ai-chat-context-keeper"
OLD_REPO = "chat_history_manager"

# Files/patterns where OLD_REPO is allowed (import path/package dir)
ALLOWLIST_OLD = [
    "src/chat_history_manager/",
    "tests/",
    "pyproject.toml",
    "docs/adr/",  # ADRs may mention legacy names historically
    "README.md",  # compatibility notes allowed
    "src/chat_history_manager/config.py",  # env compat mapping
]

def is_allowed_old(path: Path) -> bool:
    p = str(path.relative_to(ROOT))
    return any(p.startswith(a) for a in ALLOWLIST_OLD)


def main() -> int:
    violations = []
    for path in ROOT.rglob("*"):
        if path.is_dir():
            continue
        if ".git/" in str(path) or path.suffix in {".png", ".jpg", ".jpeg", ".gif", ".pdf"}:
            continue
        text: str
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        # Disallow old repo slug in contexts other than allowed
        if OLD_REPO in text and not is_allowed_old(path):
            violations.append((path, f"legacy name '{OLD_REPO}' found"))

    if violations:
        print("Naming validation failed:\n", file=sys.stderr)
        for p, msg in violations:
            print(f"- {p.relative_to(ROOT)}: {msg}")
        return 1
    print("Naming validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

