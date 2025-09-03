Development Guide (uv + pytest + ruff)

Environment

- Python managed with `uv` for fast venv and installs.
- Editable install with dev extras provides pytest, ruff, pre-commit, commitizen.

Setup

```sh
make install
make hooks
```

Everyday tasks

```sh
make lint      # ruff check
make format    # ruff format
make test      # pytest with coverage >=85%
make docs-serve  # mkdocs live server (install .[docs] first)
```

Commit Policy

- Use Conventional Commits; run `cz commit` for guided messages.
- Keep commits atomic; use `git add -p` and `git rebase -i` to curate history.

CI

- Tests: `python-tests.yml` runs on PRs and pushes to main (3.10–3.13).
- Lint: `python-lint.yml` runs ruff lint and format check.
- Commit style: `commitlint.yml` and `semantic-pr.yml`.
- Docs: `docs.yml` builds and publishes to GitHub Pages on main.

Releases

- Optional: `make cz-bump` updates version and `CHANGELOG.md` from history.
