# Workflow & Supply-chain Security

- Actions pinned to full commit SHA (no tags like `@v4`, `@main`).
- Prefer GitHub OIDC + short-lived cloud tokens over static secrets.
- Use `GITHUB_TOKEN` with least privilege where possible.
- Secrets rotation cadence: 90 days; owner: platform-team.
- Approved actions table is reviewed quarterly.

## Approved Actions (example)

| Action | Pinned SHA | Purpose | Reviewed By | Date |
|-------|------------|---------|-------------|------|
| actions/checkout | <sha> | Git checkout | platform-team | yyyy-mm-dd |

## Rationale
Pinning prevents supply-chain attacks via tag hijack. OIDC reduces secret sprawl. Rotation limits blast radius.
