# Golden Thread Traceability

This document describes how we link strategy to execution using a simple, machine‑readable map:

- Vision → OKRs → ADRs → Epics → Controls → SLOs

Artifacts

- `docs/traceability.json`: canonical, machine‑readable mapping.
- Validator: `scripts/validate_traceability.py` checks referenced ADR IDs exist.
- CI: `traceability` workflow validates on PRs and pushes.

Usage

- Add a new initiative to `docs/traceability.json` with IDs for OKRs, ADRs, epics (ticket URLs), control IDs (e.g., NIST 800‑53), and SLO IDs.
- The validator ensures that ADR IDs exist in `docs/adr/`.
