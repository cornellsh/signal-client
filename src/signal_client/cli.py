from __future__ import annotations

import argparse
import asyncio
import json

from .config import Settings
from .app import Application


async def _inspect_dlq() -> None:
    settings = Settings.from_sources()
    app = Application(settings)
    await app.initialize()
    messages = await app.dead_letter_queue.inspect()
    if not messages:
        print("Dead Letter Queue is empty.")
    else:
        print(json.dumps(messages, indent=2))
    await app.shutdown()


def inspect_dlq() -> None:
    """Synchronous entrypoint for inspecting the DLQ (test-friendly)."""
    asyncio.run(_inspect_dlq())


def main() -> None:
    parser = argparse.ArgumentParser(prog="signal-client")
    subparsers = parser.add_subparsers(dest="command")

    dlq_parser = subparsers.add_parser("dlq", help="Dead Letter Queue operations")
    dlq_subparsers = dlq_parser.add_subparsers(dest="dlq_command")
    dlq_subparsers.add_parser("inspect", help="Inspect DLQ contents")

    args = parser.parse_args()
    if args.command == "dlq" and args.dlq_command == "inspect":
        asyncio.run(_inspect_dlq())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
