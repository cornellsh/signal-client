#!/usr/bin/env bash
set -euo pipefail

echo "Running mkdocs strict build..."
poetry run mkdocs build --strict

echo "Running markdown lint (PyMarkdown)..."
poetry run pymarkdown --config .pymarkdown.json scan docs

echo "Running spell check (codespell)..."
poetry run codespell docs

echo "Docs checks complete."
