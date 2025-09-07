# Contributing

This project follows atomic commits and Conventional Commits, avoids committing personal configuration, and uses environment-first configuration with optional secrets from the OS keychain. This guide summarizes how to contribute effectively.

## Commit Policy (Atomic + Conventional Commits)

- One logical change per commit; keep commits small and self-contained.
- Messages use Conventional Commits:
  - Format: `type(scope?): subject` (imperative, ≤ 50 chars, no trailing period)
  - Types: `feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert`
  - Breaking: `type(scope)!: subject` and/or footer `BREAKING CHANGE: ...`
- Prefer interactive rebase to squash follow-ups into a single atomic commit before merge.

### Local tooling

```sh
uv pip install -e .[dev]
pre-commit install --hook-type commit-msg
cz commit        # guided commit prompts
cz bump          # optional: version + changelog
pre-commit install            # enable default hooks (ruff, hygiene)
pre-commit run -a             # run all hooks on the repo
```

### Useful git tips

```sh
git add -p                    # stage hunks by logical change
git rebase -i origin/main     # squash/fixup/reword before PR
```

## Pull Requests

- Title must follow Conventional Commits (checked in CI).
- Keep PRs focused; small and reviewable.
- Ensure CI is green. PRs run:
  - Commit-by-commit linting (`commitlint` workflow)
  - PR title check (`semantic-pr-title` workflow)

### PR template

Fill in Motivation, Changes, and Testing steps. Call out breaking changes.

## Configuration & Secrets (CNCF-aligned)

- No personal configs in Git. `.env` is ignored.
- Environment-first configuration; variables support `${VAR}` and `${VAR:-default}` interpolation.
- Prototype-friendly secrets: use OS keychain via `keyring` (optional `.[secrets]` extra).
- For Kubernetes, use External Secrets Operator to source secrets to env or files.

## Enforcing Required Status Checks (Repository Admins)

To gate merges on CI checks:

1. GitHub → Settings → Branches → Add rule (for `main`).
1. Enable: Require a pull request before merging, Dismiss stale approvals, Require status checks to pass.
1. Select required checks:
   - `commitlint`
   - `semantic-pr-title`
1. (Optional) Require linear history and/or signed commits.

## Code Style & Tests

- Lint/format via `ruff` (configured in `pyproject.toml`).
- Tests via `pytest`. Run locally:

```sh
uv pip install -e .[dev]
ruff check .                  # lint
ruff format .                 # format
pytest -q
```
