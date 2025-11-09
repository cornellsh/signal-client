---
title: Use Cases
summary: Real-world Signal bot examples that people actually build.
order: 2
---

## What people build with Signal bots

| Bot Type | What it does | Example |
| --- | --- | --- |
| **Group chat moderation** | Auto-moderate group chats, welcome new members | Delete spam, greet newcomers, enforce group rules |
| **Personal automation** | Get notifications from your servers/services | Server alerts, backup status, deployment notifications |
| **Family/friend utilities** | Shared tools for your group chats | Shopping lists, event planning, shared reminders |
| **Command bots** | Respond to commands with useful info | Weather, jokes, quick lookups, calculations |

## Real examples

### Group chat moderator bot

```python
from signal_client import SignalClient, command, Context
from signal_client.infrastructure.schemas.requests import SendMessageRequest

# Create commands using the @command decorator
@command("!welcome")
async def welcome_command(context: Context) -> None:
    """Welcome new group members"""
    welcome_msg = SendMessageRequest(
        message="👋 Welcome to the group! Please read our rules in the pinned message.",
        recipients=[]  # Recipients handled by context.send()
    )
    await context.send(welcome_msg)

@command("!rules")
async def rules_command(context: Context) -> None:
    """Show group rules"""
    rules = SendMessageRequest(
        message="""📋 Group Rules:
1. Be respectful to everyone
2. No spam or excessive self-promotion  
3. Keep discussions on-topic
4. Use threads for long conversations""",
        recipients=[]
    )
    await context.send(rules)

# Register commands with the client
client = SignalClient()
client.register(welcome_command)
client.register(rules_command)
```

### Server monitoring bot

```python
@command("!status")
async def server_status(context: Context) -> None:
    """Check server status"""
    # Your server monitoring logic here
    status = check_server_health()
    
    status_msg = SendMessageRequest(
        message=f"🖥️ Server Status: {status['status']}\n"
                f"CPU: {status['cpu']}%\n"
                f"Memory: {status['memory']}%\n"
                f"Uptime: {status['uptime']}",
        recipients=[]
    )
    await context.send(status_msg)

# Register the command
client.register(server_status)

# For scheduled tasks, you'd typically use a separate scheduler
# and send messages directly through the Signal API
```

### Family group assistant

```python
@command("!shopping")
async def shopping_list(context: Context) -> None:
    """Manage family shopping list"""
    # Simple shopping list stored in memory/file
    message_text = context.message.message or ""
    
    if message_text.startswith("!shopping add"):
        item = message_text.replace("!shopping add ", "")
        add_to_shopping_list(item)
        response = f"✅ Added '{item}' to shopping list"
    elif message_text == "!shopping list":
        items = get_shopping_list()
        response = f"🛒 Shopping List:\n" + "\n".join(f"• {item}" for item in items)
    else:
        response = "Usage: !shopping add <item> or !shopping list"
    
    reply = SendMessageRequest(message=response, recipients=[])
    await context.send(reply)

@command("!dinner")
async def dinner_poll(context: Context) -> None:
    """Quick dinner decision poll"""
    options = ["Pizza 🍕", "Chinese 🥡", "Cook at home 👨‍🍳", "Surprise me 🎲"]
    poll_msg = "🍽️ What's for dinner tonight?\n" + "\n".join(f"{i+1}. {opt}" for i, opt in enumerate(options))
    
    reply = SendMessageRequest(message=poll_msg, recipients=[])
    await context.send(reply)

# Register commands
client.register(shopping_list)
client.register(dinner_poll)
```

## Complete example with configuration

Here's a complete working bot with proper configuration:

```python
# bot.py
import asyncio
from signal_client import SignalClient, command, Context
from signal_client.infrastructure.schemas.requests import SendMessageRequest

# Configuration - put this in config.yaml or environment variables
config = {
    "signal_service": "http://localhost:8080",  # Your signal-cli-rest-api URL
    "phone_number": "+1234567890",  # Your bot's phone number
}

@command("!ping")
async def ping_command(context: Context) -> None:
    """Simple ping/pong command"""
    response = SendMessageRequest(message="🏓 Pong!", recipients=[])
    await context.send(response)

@command("!help")
async def help_command(context: Context) -> None:
    """Show available commands"""
    help_text = """🤖 Available commands:
!ping - Test if bot is working
!help - Show this help message
!weather <city> - Get weather info"""
    
    response = SendMessageRequest(message=help_text, recipients=[])
    await context.send(response)

async def main():
    # Create client with configuration
    client = SignalClient(config=config)
    
    # Register all commands
    client.register(ping_command)
    client.register(help_command)
    
    # Start the bot
    print("🤖 Signal bot starting...")
    await client.start()

if __name__ == "__main__":
    asyncio.run(main())
```

```yaml
# config.yaml (optional - you can use environment variables instead)
signal_service: "http://localhost:8080"
phone_number: "+1234567890"
worker_pool_size: 4
log_level: "INFO"
```

## Getting started

1. **Pick a simple use case** - Start with a basic command bot
2. **Set up your environment** - Follow the [Quickstart](quickstart.md) guide  
3. **Write your first command** - Use the examples above as templates
4. **Test in a private group** - Create a test group to experiment safely
5. **Deploy and iterate** - Add more features as you learn

!!! tip "Keep it simple"
    Signal bots work best when they solve specific problems for your group or personal use. Don't over-engineer - start simple and add features as needed.

> **Next step** · Learn the basics in our [Quickstart](quickstart.md) guide.
