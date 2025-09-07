# Quickstart

- Create venv: `uv venv`
- Install dev deps: `uv pip install -e .[dev]`
- Optional secrets: `uv pip install .[secrets]` (keyring)
- Enable hooks: `pre-commit install && pre-commit install --hook-type commit-msg`
- Makefile: `make lint | make format | make test | make ci`

# Save & Retrieve

- Save from stdin:
  - `pbpaste | uv run chatlog save --project-name MyProj --topic Setup --summary "Initial setup"`
- Save from a file:
  - `uv run chatlog save --project-name MyProj --topic Setup --file notes.txt`
- Retrieve latest 3:
  - `uv run chatlog retrieve --project-name MyProj --topic Setup --limit 3`
