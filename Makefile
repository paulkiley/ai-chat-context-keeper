.PHONY: help venv install hooks lint format test clean ci cz-bump docs-serve docs-build e2e smoke-staging

UV=uv
PY=$(UV) run python
PIP=$(UV) pip

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS=":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' | sort

venv: ## Create local virtual environment via uv
	$(UV) venv

install: venv ## Install project in editable mode with dev extras
	$(PIP) install -e .[dev]

hooks: ## Install pre-commit hooks (lint/format + commit-msg)
	pre-commit install
	pre-commit install --hook-type commit-msg

lint: ## Run ruff linting
	$(UV) run ruff check .

format: ## Format code with ruff
	$(UV) run ruff format .

test: ## Run pytest with coverage (min 85%)
	$(UV) run pytest -q --cov=src/chat_history_manager --cov-report=term-missing --cov-fail-under=85

ci: ## Run lint and tests (local approximation of CI)
	$(MAKE) lint
	$(MAKE) format
	$(MAKE) test

cz-bump: ## Bump version and update CHANGELOG via Commitizen
	$(UV) run cz bump

clean: ## Remove caches and artifacts
	rm -rf .pytest_cache .ruff_cache .coverage coverage.xml build dist *.egg-info

docs-serve: ## Serve mkdocs locally
	$(UV) run mkdocs serve -a 0.0.0.0:8000

docs-build: ## Build mkdocs site
	$(UV) run mkdocs build --strict

e2e: ## Run local end-to-end validation script
	bash scripts/local_e2e.sh

smoke-staging: ## Rsync real history to a staging dir and run a safe smoke test
	bash scripts/smoke_staging.sh


doctor-commits: ## Check commit messages locally (cz or commitlint)
	bash scripts/doctor_commits.sh
