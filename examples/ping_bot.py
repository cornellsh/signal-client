"""Minimal ping/pong bot to verify your Signal setup."""

from __future__ import annotations

import asyncio

from signal_client import Context, SignalClient, command


@command("!ping")
async def ping(ctx: Context) -> None:
    """Reply with a basic pong."""
    await ctx.reply_text("pong")


async def main() -> None:
    """Run the ping bot."""
    bot = SignalClient()
    bot.register(ping)
    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())
