#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_SLUG="paulkiley/ai-chat-context-keeper"
_remote_url=$(git -C "$ROOT_DIR" remote get-url origin 2>/dev/null || true)
REPO_SLUG=${REPO_SLUG:-$(printf "%s" "$_remote_url" | sed -E 's#.*github.com[:/]([^/]+/[^/.]+)(\.git)?$#\1#')}
REPO_SLUG=${REPO_SLUG:-paulkiley/ai-chat-context-keeper}

# Defaults you can override via env
OPS_PROJECT_TITLE=${OPS_PROJECT_TITLE:-"Governance & Traceability"}
OPS_Q3=${OPS_Q3:-"Q3-Foundation"}
OPS_Q4=${OPS_Q4:-"Q4-Operationalization"}

require() { command -v "$1" >/dev/null 2>&1 || { echo "Missing dependency: $1" >&2; exit 1; }; }

uv_run() {
  if command -v uv >/dev/null 2>&1; then uv run "$@"; else python "$@"; fi
}

cmd_validate() {
  pushd "$ROOT_DIR" >/dev/null
  echo "Running naming validator";     python scripts/validate_naming.py
  echo "Running ADR validator";        python scripts/validate_adrs.py
  echo "Running traceability validator"; python scripts/validate_traceability.py
  popd >/dev/null
}

cmd_docs_build() {
  require python; command -v dot >/dev/null 2>&1 || true
  pushd "$ROOT_DIR" >/dev/null
  echo "Generating decision registry & graph";
  python scripts/generate_decision_registry.py || true
  if command -v dot >/dev/null 2>&1; then dot -Tpng docs/adr/graph.dot -o docs/adr/graph.png || true; fi
  echo "Building mkdocs site";
  if ! mkdocs build; then echo "Install mkdocs: uv pip install -e .[docs]"; exit 1; fi
  popd >/dev/null
}

cmd_bench_save() {
  pushd "$ROOT_DIR" >/dev/null
  uv_run python scripts/bench_save_latency.py || true
  popd >/dev/null
}

cmd_labels() {
  require gh
  gh label create feature --color FF8C00 -d "New feature" -R "$REPO_SLUG" 2>/dev/null || true
  gh label create governance --color 1D76DB -d "Governance/ARB" -R "$REPO_SLUG" 2>/dev/null || true
  gh label create adr --color 5319E7 -d "Architecture Decision" -R "$REPO_SLUG" 2>/dev/null || true
  gh label create security --color D93F0B -d "Security/Privacy" -R "$REPO_SLUG" 2>/dev/null || true
  gh label create ci --color 0E8A16 -d "CI/CD" -R "$REPO_SLUG" 2>/dev/null || true
  gh label create docs --color 0052CC -d "Documentation" -R "$REPO_SLUG" 2>/dev/null || true
  gh label create template --color 5319E7 -d "Template/App" -R "$REPO_SLUG" 2>/dev/null || true
  gh label create app --color 0366D6 -d "Application" -R "$REPO_SLUG" 2>/dev/null || true
  gh label create framework --color 0E8A16 -d "Framework" -R "$REPO_SLUG" 2>/dev/null || true
  gh label create SLO --color 5319E7 -d "Service Level Objective" -R "$REPO_SLUG" 2>/dev/null || true
  gh label create threat-model --color D93F0B -d "Threat Model" -R "$REPO_SLUG" 2>/dev/null || true
  gh label create traceability --color 0052CC -d "Traceability" -R "$REPO_SLUG" 2>/dev/null || true
}

cmd_milestones() {
  require gh
  gh api repos/$REPO_SLUG/milestones -X POST -f title='Q3-Foundation' -f state='open' -f description='Foundation: governance, ADRs, registry, traceability' >/dev/null 2>&1 || true
  gh api repos/$REPO_SLUG/milestones -X POST -f title='Q4-Operationalization' -f state='open' -f description='Operationalization: measurement, threat model, SLOs, enhancements' >/dev/null 2>&1 || true
}

cmd_project_create() {
  require gh
  echo "Creating user Project (new Projects)…"
  if ! gh project create --owner @me --title "Governance & Traceability" --format json -q .number; then
    echo "Could not create project. Ensure scopes: gh auth refresh -s project,read:project" >&2
    exit 1
  fi
}

cmd_project_add_backlog() {
  require gh
  local proj_number="${1:-}"
  if [[ -z "$proj_number" ]]; then echo "Usage: ops.sh project-add-backlog <project-number>" >&2; exit 2; fi
  echo "Adding Q3-Foundation issues to project $proj_number"
  local urls
  urls=$(gh issue list -R "$REPO_SLUG" --state open --milestone "$OPS_Q3" --json url -q '.[].url')
  while IFS= read -r url; do
    [[ -z "$url" ]] && continue
    gh project item-add --project "$proj_number" --url "$url" || true
  done <<< "$urls"
}

cmd_help() {
  cat <<EOF
Usage: scripts/ops.sh <command>

Commands:
  validate           Run local validators (naming, ADR, traceability)
  docs-build         Generate registry/graph and build docs locally
  bench-save         Measure local save latency
  labels             Create standard labels (idempotent)
  milestones         Create Q3/Q4 milestones (idempotent)
  project-create     Create user project (requires gh scopes project,read:project)
  project-add-backlog <project-number>  Add Q3 backlog issues to the project
  project-sync       Auto-find or create the project by title and add Q3 backlog
  pr --title "…" [--labels "…"] [--milestone "…"] [--base main]
                     Create a PR with one command (auto-labels by title if omitted)
  help               Show this help

Notes:
  Refresh GH scopes if needed: gh auth refresh -s project,read:project
EOF
}

case "${1:-help}" in
  validate) shift; cmd_validate "$@" ;;
  docs-build) shift; cmd_docs_build "$@" ;;
  bench-save) shift; cmd_bench_save "$@" ;;
  labels) shift; cmd_labels "$@" ;;
  milestones) shift; cmd_milestones "$@" ;;
  project-create) shift; cmd_project_create "$@" ;;
  project-add-backlog) shift; cmd_project_add_backlog "$@" ;;
  project-sync) shift; cmd_project_sync "$@" ;;
  pr) shift; cmd_pr_create "$@" ;;
  help|*) cmd_help ;;
esac
