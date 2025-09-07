## Summary

Briefly describe the change and its intent.

## Motivation

Why is this change needed? Link issues if applicable.

## Changes

- What changed at a high level?
- Any breaking changes? If yes, explain impact and migration.

## Testing

- How did you test this change?
- Include commands or steps to validate.

## Checklist

- [ ] Conventional Commit PR title (e.g., `feat(config): add env interpolation`)
- [ ] Small, atomic diff; unrelated changes split out
- [ ] CI green (commitlint + PR title)
- [ ] No secrets or personal configs added

## Self-Review Checklist (Solo Operator)

*As the sole contributor, I am acting as my own peer reviewer. I confirm I have completed the following before approving this PR:*

- [ ] **Cooling-Off Period:** Took a 30+ minute break between writing and reviewing.
- [ ] **Line-by-Line Review:** Re-read the entire diff.
- [ ] **Local Validation:** Ran local checks (`make doctor-commits`, `make validate` or equivalent) and they pass.
- [ ] **ADR Compliance:** Reviewed relevant ADRs or added/updated one if introducing a decision.
- [ ] **Threat Model Consideration:** Considered security implications.
- [ ] **Clarity for Future Me:** Title, description, and comments capture the “why” clearly.
