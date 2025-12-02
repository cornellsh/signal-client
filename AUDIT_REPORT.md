# Signal Client Codebase Audit
_Most recent review delivered with a senior engineer mindset: this audit documents structure, tooling, naming, and configuration along with concrete, high-impact concerns that still need attention._

## 1. Scope & Methodology
- Triage the repository shape (`pyproject.toml`, `src/`, `tests/`, `scripts/`, `AGENTS.md`) to understand ownership and workflow expectations.
- Read key runtime modules (`bot.py`, `worker_pool_manager.py`, `message_service.py`, `container.py`, `websocket_client.py`) plus the supporting tests to see how features are exercised.
- Identify mismatches between documented process (README/AGENTS) and actual implementation plus structural/design risks that could bite future maintainers.

## 2. Project Layout & Naming
- **Source layout:** `src/signal_client/` holds the bot/domain surfaces (`bot.py`, `command.py`, `context.py`, `metrics.py`) grouped by concept, with services/infra storage split into submodules. Naming adheres to snake_case modules and PascalCase classes.
- **Dependency injection:** `container.py` wires everything via `dependency_injector`. Services depend on `Settings`, and the hierarchy (Container → ServicesContainer → storage/api clients) follows the AGENTS guidance about grouped surfaces.
- **Tests-as-docs:** `tests/` mirrors the runtime structure (`services/`, `infrastructure/`, `integration/`), so the suite doubles as documentation as described in `README.md`. Integration tests (e.g., `tests/integration/test_end_to_end.py`) cover orchestration layers; targeted unit tests in `tests/services/` exercise core helpers.
- **Tooling:** `pyproject.toml` defines Poetry-managed runtime/dev dependencies, Ruff/mypy configurations, semantic-release hooks, and custom scripts (`pytest-safe`, `audit-api`, `release_guard`) matching the desired workflow.

## 3. Architecture & Behavior Insights
- The runtime is event-driven: `SignalClient` wires `MessageService` → queue → `WorkerPoolManager`, with `Context` objects instantiated per message via `dependency_injector`. Worker pool owns middleware execution and command dispatch, while metrics (`MESSAGE_QUEUE_*`) are emitted within the worker loop.
- `MessageService` does the heavy lifting of listening on `WebSocketClient`, applying backpressure (with optional oldest-message drop), and optionally persisting failed enqueues to a dead-letter queue.
- Services such as rate limiting, locking, and circuit breaking live in `src/signal_client/services/` and are wired through the `ServicesContainer`—there are no module-level singletons outside the DI graph, which matches the coding rules.

## 4. Deep Findings (constructive critique)

### 1. Trigger compilation conflicts make longer triggers unreachable once shorter ones exist
`WorkerPoolManager._compile_triggers` builds two regexes that are literally `(|)`, sorted lexicographically (`src/signal_client/services/worker_pool_manager.py:212-241`). Because `.match()` is used later, any text beginning with a shorter trigger (e.g., `!ping`) will always match that trigger before a longer but related one (`!pingpong`) can be considered. The sorted list (alphabetical) further biases the order, so developers cannot safely add prefix-based commands. Consider anchoring each trigger (for example `rf"(?P<t>{re.escape(trigger)})"`) and/or sorting by descending length before building the combined regex so longer triggers win.

### 2. Dynamic command registration freezes after `start()`
`SignalClient.register` and `WorkerPoolManager.register` mutate shared command dictionaries, but `_compile_triggers()` (and `_sensitive/insensitive_regex`) are only executed in `WorkerPoolManager.start()` (`src/signal_client/services/worker_pool_manager.py:195-235`). Once the worker pool starts, adding another command via `SignalClient.register` updates `_commands`, but the previously compiled regex continues to drive `_select_command`. The new command’s trigger is never matched, so runtime extensions (e.g., feature-flagged commands registered post-start) silently disappear. Either disallow registering after start (and surface an error) or rerun `_compile_triggers()` / update each worker when new commands arrive.

### 3. Regex command registrations are captured by value at worker creation
`Worker.__init__` receives a copy of the regex command list (`self._regex_commands = list(config.regex_commands)` on `src/signal_client/services/worker_pool_manager.py:56-64`). Because this copy happens when the worker starts, any regex command registered afterwards (e.g., through `SignalClient.register` during runtime) is appended to `WorkerPoolManager._regex_commands` but never propagated to existing `Worker` instances. In practice this means regex-style commands are effectively immutable once the pool has started. The worker should either hold a shared reference or be notified to refresh its list whenever `WorkerPoolManager` receives new regex commands.

### 4. WebSocket reconnection loop is brittle outside of clean closures
`WebSocketClient.listen` curves through `ConnectionClosed` but does not catch `OSError`, `InvalidHandshake`, `WebSocketException`, or any other raised exception (`src/signal_client/infrastructure/websocket_client.py:28-54`). Those errors come up during the first connect or if an upstream proxy resets the socket; because they escape the loop, the generator ends, the queue stops receiving, and the entire bot goes silent without structured logging or recovery. The code should catch `Exception` (at least `websockets.WebSocketException` and `OSError`), log it, and keep retrying with the exponential backoff already in place. Without this safeguard, production Signal outages or transient DNS glitches immediately halt the bot.

### 5. Release tooling claims require missing artifacts
`pyproject.toml` references `CHANGELOG.md` in the `semantic_release.changelog` section, but the repository currently lacks that file (`ls` output). When `python -m semantic_release publish` runs or CI expects the changelog, it will crash before packaging. Please commit a maintained `CHANGELOG.md` (or adjust the release config to generate it) so the release guard and CI scripts are aligned with reality.

### 6. README's “tests as documentation” claim needs the missing guidance referenced in AGENTS
AGENTS.md emphasizes that `tests/` are living documentation, but the README only points to `tests/` in a general sense. There’s no section describing how to inspect the test tree, how to run the quick loops (`pytest -m "not performance"`), nor how to interpret the load/performance markers. Adding a short “Testing as Documentation” section that highlights where to look for command wiring (`tests/services/`), infrastructure dependencies (`tests/infrastructure/`), and opt-in performance checks (`tests/test_performance.py`) would make the README back up the stated approach and help new contributors orient themselves.

## 5. Tooling & Process Notes
- `pip-audit` is mentioned under “Operations” in README but is not wired as a Poetry script or enforced via CIP (pyproject only lists lint/mypy/pytest-safe). Consider adding a `[tool.poetry.scripts]` entry (e.g., `pip-audit = "pip_audit:main"`) or a `scripts/pip_audit.py` so the promised security gate is trivially runnable locally and within CI.
- There is no `tests/test_performance.py` marker description in README; since the file runs opt-in jobs, document how to run/skip it explicitly (e.g., “skip via `pytest -m "not performance"` or `pytest tests/test_performance.py` with `PYTEST_ADDOPTS`”).
- The `AGENTS.md` instructions around compatibility (`python -m signal_client.compatibility --strict`) are satisfied by `compatibility.py`, but there is no mention of how that script reports success/failure; consider documenting sample output or exit codes in README to make the gating clearer.

## 6. Recommendations
1. Fix the worker trigger regex builder so longer triggers cannot be shadowed and support runtime additions (recompile/update workers or fail on post-start registration).
2. Harden `WebSocketClient.listen` by catching broader connection errors and continuing to retry; log the failure so operators understand why the listener restarted.
3. Add the missing `CHANGELOG.md`, or adapt `semantic_release.changelog` so the release guard stops depending on a nonexistent file.
4. Expand README sections about the living tests/documentation, the quick `pytest` loop, and the compatibility gate so contributors can reproduce the stated workflow.
5. Introduce a `pip-audit` script entry (and optionally mention it in README) so the security gate in the operations section is actionable without digging through CI.

## 7. Next Steps
- Share and prioritize the findings above with the team. The Worker/regex issues should be addressed before shipping new commands or middleware, so the runtime behaves predictably.
- Document the enhanced README/testing instructions and hook up the release/security tooling so that contributors don’t have to reverse-engineer the existing process.
- After adjustments, rerun `pytest-safe` (and optionally `bandit`, `pip-audit`, `python -m signal_client.compatibility --strict`) to update the audit status.
