# Release & Publishing

Steps to ship a new version with confidence.

## Quality gates
Run these before cutting a release:

```bash
poetry check
poetry run ruff check .
poetry run mypy src
poetry run pytest
poetry run mkdocs build
```

## Packaging
- Build artifacts: `poetry build` (produces wheel + sdist under `dist/`).
- Verify locally: `python -m pip install dist/signal_client-<version>-py3-none-any.whl` in a clean virtualenv and run a quick example (`poetry run python examples/ping_bot.py` with your env vars set).

## Semantic release
- Conventional commits drive versioning via `python-semantic-release` (configured in `pyproject.toml`, branch: `main`).
- Typical flow:
  ```bash
  poetry run semantic-release version  # bumps version + changelog
  poetry run semantic-release publish  # builds and uploads to PyPI/releases
  ```
- Keep CI configured with the necessary PyPI credentials and GitHub token for publishing.

## Docs publishing
- Validate site: `poetry run mkdocs build`
- Publish to GitHub Pages (if configured): `poetry run mkdocs gh-deploy --clean`
- The README links to https://cornellsh.github.io/signal-client/; keep it in sync after each release.
