# Pull Request Ordering & Safety

This repository enforces safe merge order for dependent PRs. A CI workflow (`pr-order`) reads `.github/pr-deps.json` and blocks merging if a dependency has not been merged yet.

## How it works

- `.github/pr-deps.json` maps branch names to dependencies:

```json
{
  "chore/doctor-ci": { "depends_on": ["chore/make-init-pr"] }
}
```

- On each PR, the workflow checks if the PR’s branch is listed, finds the dependent PR(s) targeting the same base, and verifies they are merged.
- If not merged, CI fails with a clear message.

## Local triage (copy/paste)

```sh
# See open PRs and their branches
gh pr list -L 20 --json number,headRefName,title,labels,state -q '.[] | "#\(.number)\t\(.headRefName)\t\(.title)"'

# See which PRs touch hot files (Makefile, scripts/ops.sh)
for n in $(gh pr list --state open --json number -q '.[].number'); do \
  echo "#${n}"; gh pr view $n --json files -q '.files[].path' | rg '^(Makefile|scripts/ops\.sh)$' || true; \
 done

# Check dependency for the current branch in pr-deps.json
cat .github/pr-deps.json | jq -r 'to_entries[] | "\(.key): depends_on=\(.value.depends_on|join(","))"'
```

## Common failure modes

- Merging dependent PR first: CI fails with “Dependency PR is not merged yet.” Merge the prerequisite PR and re-run CI.
- Exec bit regression on `scripts/ops.sh`: if a later PR changes file mode back to 100644, re-add exec bit and push:

```sh
git update-index --chmod=+x scripts/ops.sh
git commit -m "chore(ops): restore exec bit"
```

- Conflicting edits in `Makefile` or `scripts/ops.sh`: rebase dependent PR on main, resolve conflicts, and push with `--force-with-lease`.

## Chaos engineering (learn-by-breaking)

- Intentionally swap merge order in a test branch; confirm the `pr-order` job fails and blocks merge.
- Remove a dependency mapping and create both PRs; add the mapping and watch CI enforce order.
- Add a fake dependency branch name; verify CI fails with “Dependency PR not found.”

These scenarios help teams learn the safety net and how to recover quickly.
