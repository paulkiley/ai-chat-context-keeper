#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADR_DIR = ROOT / "docs" / "adr"

TITLE_RE = re.compile(r"^#\s+(\d+)\.\s+(.+)$")
STATUS_HDR = re.compile(r"^##\s+Status$", re.IGNORECASE)
META_HDR = re.compile(r"^##\s+Metadata$", re.IGNORECASE)


@dataclass
class AdrEntry:
    id: str
    title: str
    status: str
    supersedes: list[str]
    depends_on: list[str]
    informs: list[str]
    path: str


def parse_metadata(lines: list[str]) -> dict[str, list[str]]:
    meta = {"supersedes": [], "depends_on": [], "informs": []}
    try:
        start = next(i for i, ln in enumerate(lines) if META_HDR.match(ln.strip()))
    except StopIteration:
        return meta
    for ln in lines[start + 1 : start + 20]:
        s = ln.strip()
        if s.startswith("- supersedes:"):
            val = s.split(":", 1)[1].strip().strip("[]")
            meta["supersedes"] = [x.strip() for x in val.split(",") if x.strip()]
        elif s.startswith("- depends_on:"):
            val = s.split(":", 1)[1].strip().strip("[]")
            meta["depends_on"] = [x.strip() for x in val.split(",") if x.strip()]
        elif s.startswith("- informs:"):
            val = s.split(":", 1)[1].strip().strip("[]")
            meta["informs"] = [x.strip() for x in val.split(",") if x.strip()]
        elif s.startswith("## "):
            break
    return meta


def parse_status(lines: list[str]) -> str:
    try:
        idx = next(i for i, ln in enumerate(lines) if STATUS_HDR.match(ln.strip()))
    except StopIteration:
        return "Unknown"
    for ln in lines[idx + 1 : idx + 5]:
        s = ln.strip()
        if s:
            return s
    return "Unknown"


def collect() -> list[AdrEntry]:
    entries: list[AdrEntry] = []
    for path in sorted(ADR_DIR.glob("*.md")):
        lines = path.read_text(encoding="utf-8").splitlines()
        if not lines:
            continue
        m = TITLE_RE.match(lines[0].strip())
        if not m:
            continue
        adr_id, title = m.group(1), m.group(2)
        status = parse_status(lines)
        meta = parse_metadata(lines)
        entries.append(
            AdrEntry(
                id=adr_id,
                title=title,
                status=status,
                supersedes=meta["supersedes"],
                depends_on=meta["depends_on"],
                informs=meta["informs"],
                path=str(path.relative_to(ROOT)),
            )
        )
    return entries


def write_registry(entries: list[AdrEntry]) -> Path:
    out = ADR_DIR / "registry.json"
    out.write_text(json.dumps([asdict(e) for e in entries], indent=2), encoding="utf-8")
    return out


def write_dot(entries: list[AdrEntry]) -> Path:
    lines = ["digraph ADR {", "rankdir=LR;"]
    # Nodes
    for e in entries:
        label = f"{e.id}: {e.title.replace('"', '\\"')}\n({e.status})"
        lines.append(f'  "{e.id}" [label="{label}"];')
    # Edges
    for e in entries:
        for dep in e.depends_on:
            lines.append(f'  "{dep}" -> "{e.id}" [label="depends"];')
        for sup in e.supersedes:
            lines.append(f'  "{sup}" -> "{e.id}" [label="supersedes", color="blue"];')
    lines.append("}")
    dot = ADR_DIR / "graph.dot"
    dot.write_text("\n".join(lines), encoding="utf-8")
    return dot


def main() -> int:
    entries = collect()
    write_registry(entries)
    write_dot(entries)
    print(f"Wrote registry and dot for {len(entries)} ADRs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

