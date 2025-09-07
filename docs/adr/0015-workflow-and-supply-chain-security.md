# 15. workflow and supply chain security

Date: 2025-09-07

## Status
Accepted

## Context
All GitHub Actions must be pinned to full commit SHAs. Prefer OIDC and short-lived tokens over long-lived secrets; rotate secrets at least every 90 days. All validator scripts under scripts/ used by CI are Tier-1 governance code, included in CODEOWNERS, and subject to security review (SAST + human review by platform/security).

## Decision
[Summarize the decision concisely.]

## Consequences
[List positive/negative tradeoffs.]

## Metadata
- supersedes: []
- depends_on: []
- informs: []

## Security & Privacy Considerations
[Outline any implications; references to threat model if applicable.]
