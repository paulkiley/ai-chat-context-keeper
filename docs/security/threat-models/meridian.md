# Threat Model: Meridian Knowledge Platform

Scope

- Centralized knowledge base aggregating ADRs, docs, and (future) chat context.

Assets & Data Classification

- ADRs/docs (internal): low/medium sensitivity.
- Chat context: potentially sensitive; classify and minimize.

Trust Boundaries

- Ingestion pipeline; storage at rest; access via docs site or API.

Threats (STRIDE)

- Spoofing (unauthorized access), Tampering (corrupted index), Repudiation (lack of audit),
  Information Disclosure (sensitive context leakage), DoS (index build), Elevation of Privilege.

Controls (baseline)

- NIST-800-53:SC-28 (encryption at rest), AU-2 (audit events), IA-2 (authentication), AC-3 (access enforcement).

Design Notes

- Keep Context Keeper local by default; explicit ADR approval for centralization.
- Retention policies enforced; redaction where possible; access logs retained.
