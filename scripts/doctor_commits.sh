#!/usr/bin/env bash
set -euo pipefail

base=${1:-}
if [[ -z "${base}" ]]; then
  base=$(git merge-base HEAD origin/main 2>/dev/null || echo origin/main)
fi

echo "Commit range: ${base}..HEAD"
status=0
if command -v cz >/dev/null 2>&1; then
  echo "Using Commitizen to check history..."
  if ! cz check --rev-range "${base}..HEAD"; then status=1; fi
elif command -v npx >/dev/null 2>&1; then
  echo "Using commitlint to check history..."
  if ! npx --yes commitlint --from "${base}" --to HEAD; then status=1; fi
else
  echo "No checker found. Install one of:\n  - uv pip install -e .[dev]   # provides commitizen\n  - npm i -D @commitlint/cli @commitlint/config-conventional" >&2
  exit 2
fi

if [[ $status -ne 0 ]]; then
  cat <<'EOF'
Not compliant. Options to fix:
- Interactive rebase:   git rebase -i origin/main   # mark commits as 'reword'
- Squash to one commit: git reset --soft origin/main && git commit -m "type(scope): subject" -m "body..." && git push --force-with-lease
EOF
else
  echo "Commit messages OK."
fi
exit $status
