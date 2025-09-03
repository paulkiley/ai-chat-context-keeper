# Solo Operator Governance Model

When a non-author reviewer is not available, we adapt the framework to preserve deliberate reviews:

- **CI as Peer Reviewer:** No PR merges unless all required checks are green.
- **Self-Approval Protocol:** Author self-approves only after completing the Self-Review Checklist in the PR.
- **CODEOWNERS:** Critical paths auto-assign the platform-team (currently @paulkiley) to ensure heightened scrutiny.
- **Break-Glass:** Admin merges permitted only for time-sensitive critical fixes when designated approvers are unavailable; ARB review within 1 business day.

See the PR template for the mandatory checklist.
