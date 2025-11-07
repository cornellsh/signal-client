---
title: Coding Standards
summary: Keep contributions consistent, reliable, and review-friendly.
order: 300
---

## Style checklist

- Run `ruff check --fix` and `black` before committing.
- Name async commands with verbs (`handle_ticket`, `broadcast_status`).
- Keep configuration parsing in `signal_client.config`; avoid duplicating env logic in commands.
- Write docstrings for public APIs and CLI entry points.[^docstrings]

!!! info "Commit etiquette"
    Use Conventional Commit prefixes (`feat:`, `fix:`, `docs:`) so automated release tooling can cut changelogs without manual intervention.

## Testing expectations

1. Add unit tests under `tests/unit/` for new services or utilities.
2. Use `pytest --asyncio-mode=auto` to cover async commands.
3. Mock Signal REST endpoints with `aresponses` fixtures.
4. Gate merges on `pytest-safe` (wrapper script running coverage, type checks, and linting).

## Review checklist

- [ ] Command names are descriptive and idempotent.
- [ ] Exceptions bubble to the runtime (no broad `except Exception`).
- [ ] Metrics and logs follow existing naming conventions.
- [ ] Configuration changes include documentation updates.

[^docstrings]: Docstrings are ignored by the linter, but they must still explain intent for maintainers and recruiters reviewing the repository.
